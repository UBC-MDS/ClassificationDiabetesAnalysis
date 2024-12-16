# preprocessing_model_fitting.py
# author: Javier Martinez
# date: 2024-12-05

# Usage:
# python scripts/preprocessing_model_fitting.py \
#     --processed-dir ./data/processed \
#     --results-dir ./results/tables

import os
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from scipy.stats import loguniform
import click
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_csv_data import read_csv_data
from src.save_csv_data import save_csv_data
from src.save_model import save_model


@click.command()
@click.option('--processed-dir', type=str, help="Path to the directory containing processed data")
@click.option('--results-dir', type=str, help="Path to the directory where results will be saved")
def main(processed_dir, results_dir):
    """
    Main function to load data, calculate dummy score, and optimize Logistic Regression.

    Parameters:
    ----------
    processed_dir : str
        Directory containing processed X_train, y_train CSV files.
    results_dir : str
        Directory to save the models and results.
    """
    # Load training data
    X_train = read_csv_data(os.path.join(processed_dir, 'X_train.csv'))
    y_train = read_csv_data(os.path.join(processed_dir, 'y_train.csv'))['Outcome']

    # Calculate Dummy Classifier's cross-validation score
    dummy_clf = DummyClassifier(strategy="most_frequent")
    mean_cv_score = cross_val_score(dummy_clf, X_train, y_train, cv=5).mean()

    # Save the Dummy Classifier's mean CV score
    os.makedirs(os.path.join(results_dir, 'tables'), exist_ok=True)
    dummy_score_path = os.path.join(results_dir, 'tables', 'mean_cv_score.csv')
    save_csv_data(pd.DataFrame({'mean_cv_score': [mean_cv_score]}), dummy_score_path)

    # Optimize Logistic Regression
    log_pipe = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=123)
    )

    param_dist = {"logisticregression__C": loguniform(1e-5, 1e+5)}
    random_search = RandomizedSearchCV(
        log_pipe, param_dist, n_iter=20, n_jobs=-1, cv=5, return_train_score=True, random_state=123
    )
    random_fit = random_search.fit(X_train, y_train)

    # Save the pipeline and RandomizedSearchCV results using save_model
    save_model(log_pipe, os.path.join(results_dir, 'models', 'log_pipe.pkl'))
    save_model(random_fit, os.path.join(results_dir, 'models', 'random_fit.pkl'))

    # Save best parameters
    best_params_path = os.path.join(results_dir, 'tables', 'best_params.csv')
    save_csv_data(pd.DataFrame([random_search.best_params_]), best_params_path)


if __name__ == '__main__':
    main()

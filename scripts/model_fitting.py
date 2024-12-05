# model_fitting.py
# author: Javier Martinez
# date: 2024-12-05

import os
import pandas as pd
import numpy as np
import pickle
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from scipy.stats import loguniform
import click


@click.command()
@click.option('--processed-dir', type=str, help="Path to the directory containing processed data")
@click.option('--results-dir', type=str, help="Path to the directory where results will be saved")
def main(processed_dir, results_dir):
    """
    Fits a Logistic Regression model with hyperparameter optimization and evaluates it.

    Parameters:
    ----------
    processed_dir : str
        Directory containing processed X_train, y_train, X_test, and y_test CSV files.
    results_dir : str
        Directory to save the model and results.

    Outputs:
    --------
    Saves mean_cv_score as a CSV file in ../results/tables/
    Saves log_pipe and random_search as pickle objects in ../results/models/
    """
    os.makedirs(os.path.join(results_dir, 'tables'), exist_ok=True)
    os.makedirs(os.path.join(results_dir, 'models'), exist_ok=True)

    # Load processed data
    X_train = pd.read_csv(os.path.join(processed_dir, 'X_train.csv'))
    y_train = pd.read_csv(os.path.join(processed_dir, 'y_train.csv'))['Outcome']

    # Dummy Classifier and cross-validation
    dummy_clf = DummyClassifier(strategy="most_frequent")
    mean_cv_score = cross_val_score(dummy_clf, X_train, y_train, cv=5).mean()

    # Save mean_cv_score
    pd.DataFrame({'mean_cv_score': [mean_cv_score]}).to_csv(
        os.path.join(results_dir, 'tables', 'mean_cv_score.csv'), index=False)

    # Logistic Regression Pipeline and RandomizedSearchCV
    log_pipe = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=123)
    )
    param_dist = {
        "logisticregression__C": loguniform(1e-5, 1e+5)
    }
    random_search = RandomizedSearchCV(
        log_pipe, param_dist, n_iter=20, n_jobs=-1, cv=5, return_train_score=True, random_state=123
    )
    random_search.fit(X_train, y_train)

    # Save log_pipe and random_search as pickle objects
    with open(os.path.join(results_dir, 'models', 'log_pipe.pkl'), 'wb') as f:
        pickle.dump(log_pipe, f)
    with open(os.path.join(results_dir, 'models', 'random_search.pkl'), 'wb') as f:
        pickle.dump(random_search, f)


if __name__ == '__main__':
    main()

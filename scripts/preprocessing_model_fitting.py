# preprocessing_model_fitting.py
# author: Javier Martinez
# date: 2024-12-05

import os
import pandas as pd
import pickle
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import cross_val_score, RandomizedSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from scipy.stats import loguniform
import click


def load_data(processed_dir):
    """
    Loads training data from the processed directory.

    Parameters:
    -----------
    processed_dir : str
        Path to the directory containing processed data.

    Returns:
    --------
    tuple
        X_train (pd.DataFrame): Features for the training set.
        y_train (pd.Series): Target variable for the training set.
    """
    X_train = pd.read_csv(os.path.join(processed_dir, 'X_train.csv'))
    y_train = pd.read_csv(os.path.join(processed_dir, 'y_train.csv'))['Outcome']
    return X_train, y_train


def calculate_dummy_score(X_train, y_train, results_dir):
    """
    Calculates the mean cross-validation score for a DummyClassifier and saves it.

    Parameters:
    -----------
    X_train : pd.DataFrame
        Features for the training set.
    y_train : pd.Series
        Target variable for the training set.
    results_dir : str
        Path to the directory where results will be saved.

    Returns:
    --------
    float
        Mean cross-validation score for the DummyClassifier.
    """
    dummy_clf = DummyClassifier(strategy="most_frequent")
    mean_cv_score = cross_val_score(dummy_clf, X_train, y_train, cv=5).mean()

    # Save mean CV score
    os.makedirs(os.path.join(results_dir, 'tables'), exist_ok=True)
    pd.DataFrame({'mean_cv_score': [mean_cv_score]}).to_csv(
        os.path.join(results_dir, 'tables', 'mean_cv_score.csv'),
        index=False
    )

    return mean_cv_score


def optimize_logistic_regression(X_train, y_train, results_dir):
    """
    Performs hyperparameter optimization for Logistic Regression and saves the results.

    Parameters:
    -----------
    X_train : pd.DataFrame
        Features for the training set.
    y_train : pd.Series
        Target variable for the training set.
    results_dir : str
        Path to the directory where models and parameters will be saved.

    Returns:
    --------
    tuple
        - log_pipe (Pipeline): Logistic Regression pipeline.
        - random_fit (RandomizedSearchCV): Fitted RandomizedSearchCV object.
    """
    log_pipe = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=2000, random_state=123)
    )

    param_dist = {"logisticregression__C": loguniform(1e-5, 1e+5)}
    random_search = RandomizedSearchCV(
        log_pipe, param_dist, n_iter=20, n_jobs=-1, cv=5, return_train_score=True, random_state=123
    )
    random_fit = random_search.fit(X_train, y_train)

    # Save the pipeline and random search results
    os.makedirs(os.path.join(results_dir, 'models'), exist_ok=True)
    with open(os.path.join(results_dir, 'models', 'log_pipe.pkl'), 'wb') as f:
        pickle.dump(log_pipe, f)
    with open(os.path.join(results_dir, 'models', 'random_fit.pkl'), 'wb') as f:
        pickle.dump(random_fit, f)

    # Save best parameters
    best_params = random_search.best_params_
    pd.DataFrame([best_params]).to_csv(
        os.path.join(results_dir, 'tables', 'best_params.csv'),
        index=False
    )

    return log_pipe, random_fit


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
    # Load the training data
    X_train, y_train = load_data(processed_dir)

    # Calculate and save the Dummy Classifier's cross-validation score
    calculate_dummy_score(X_train, y_train, results_dir)

    # Optimize Logistic Regression and save the models and results
    optimize_logistic_regression(X_train, y_train, results_dir)


if __name__ == '__main__':
    main()

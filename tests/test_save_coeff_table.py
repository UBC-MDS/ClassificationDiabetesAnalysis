import pytest
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import os
from src.save_coeff_table import save_coefficients_table

def test_save_coefficients_table_success(tmp_path):
    # Create X_train and y_train
    X_train = pd.DataFrame({
        'feature1': [1, 2, 3, 4],
        'feature2': [2, 3, 4, 5]
    })
    y_train = [0, 1, 0, 1]
    # Create and train the model
    model = Pipeline([('logisticregression', LogisticRegression())])
    model.fit(X_train, y_train)

    # Temporary directory for saving results
    results_to = tmp_path

    # Call the function
    save_coefficients_table(model, X_train, results_to)

    # Validate the results
    saved_file = os.path.join(results_to, "coeff_table.csv")
    assert os.path.exists(saved_file)
    coeff_df = pd.read_csv(saved_file)
    assert 'Features' in coeff_df.columns
    assert 'Coefficients' in coeff_df.columns
    assert len(coeff_df) == X_train.shape[1]


def test_save_coefficients_table_empty_X_train(tmp_path):
    # Create an empty DataFrame for X_train
    X_train = pd.DataFrame()

    # Create the model (not trained because X_train is empty)
    model = Pipeline([('logisticregression', LogisticRegression())])

    # Temporary directory for saving results
    results_to = tmp_path

    # Expect ValueError due to empty X_train
    with pytest.raises(ValueError, match="Model is not trained. Please train the model before extracting coefficients."):
        save_coefficients_table(model, X_train, results_to)


def test_save_coefficients_table_invalid_X_train_type(tmp_path):
    # Pass a list instead of a DataFrame for X_train
    X_train = [1, 2, 3, 4]

    # Create the model
    model = Pipeline([('logisticregression', LogisticRegression())])

    # Temporary directory for saving results
    results_to = tmp_path

    # Expect TypeError due to incorrect X_train type
    with pytest.raises(TypeError, match="X_train should be a pandas DataFrame"):
        save_coefficients_table(model, X_train, results_to)

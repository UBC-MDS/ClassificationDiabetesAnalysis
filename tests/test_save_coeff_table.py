import pytest
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from src.save_coeff_table import save_coefficients_table

def test_save_coefficients_table_valid_case(tmp_path):
    # Create a valid DataFrame for X_train
    X_train = pd.DataFrame({
        'feature1': np.random.rand(10),
        'feature2': np.random.rand(10)
    })

    # Create and train a logistic regression model
    model = Pipeline([
        ('logisticregression', LogisticRegression())
    ])
    model.fit(X_train, np.random.randint(0, 2, size=10))

    # Temporary directory for saving results
    results_to = tmp_path

    # Call the function and check the output
    coeff_df = save_coefficients_table(model, X_train, results_to)

    # Assert that the CSV file was created
    csv_path = tmp_path / "coeff_table.csv"
    assert csv_path.exists(), "CSV file was not created"

    # Assert the DataFrame has the correct structure
    assert list(coeff_df.columns) == ['Features', 'Coefficients'], "DataFrame columns are incorrect"
    assert len(coeff_df) == X_train.shape[1], "Number of coefficients does not match number of features"

def test_save_coefficients_table_empty_X_train(tmp_path):
    # Create an empty DataFrame for X_train
    X_train = pd.DataFrame()

    # Create the model (not trained because X_train is empty)
    model = Pipeline([('logisticregression', LogisticRegression())])

    # Temporary directory for saving results
    results_to = tmp_path

    # Expect ValueError due to empty X_train
    with pytest.raises(ValueError, match="Model is not trained or does not have coefficients."):
        save_coefficients_table(model, X_train, results_to)

def test_save_coefficients_table_missing_logisticregression(tmp_path):
    # Create a valid DataFrame for X_train
    X_train = pd.DataFrame({
        'feature1': np.random.rand(10),
        'feature2': np.random.rand(10)
    })

    # Create a pipeline without 'logisticregression'
    model = Pipeline([
        ('otherstep', LogisticRegression())
    ])

    # Temporary directory for saving results
    results_to = tmp_path

    # Expect ValueError due to missing 'logisticregression' step
    with pytest.raises(ValueError, match="'logisticregression' step not found in the pipeline."):
        save_coefficients_table(model, X_train, results_to)


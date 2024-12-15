import sys
import os
import pytest
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.preprocessing_model_fitting import load_data, calculate_dummy_score, optimize_logistic_regression


@pytest.fixture
def sample_data():
    """Fixture for creating sample datasets."""
    X_train = pd.DataFrame({
        "Feature1": [1.0, 2.0, 3.0, 4.0],
        "Feature2": [5.0, 6.0, 7.0, 8.0]
    })
    y_train = pd.DataFrame({"Outcome": [0, 1, 0, 1]})
    return X_train, y_train


def test_load_data(sample_data, tmp_path):
    """
    Test load_data to ensure X_train and y_train have the same number of rows.
    """
    X_train, y_train = sample_data

    # Create temporary directory and save X_train and y_train
    processed_dir = tmp_path / "processed"
    processed_dir.mkdir()
    X_train.to_csv(processed_dir / "X_train.csv", index=False)
    y_train.to_csv(processed_dir / "y_train.csv", index=False)

    # Use load_data to load the datasets
    loaded_X_train, loaded_y_train = load_data(str(processed_dir))

    # Assert that row counts match
    assert loaded_X_train.shape[0] == loaded_y_train.shape[0], "X_train and y_train do not have the same number of rows"


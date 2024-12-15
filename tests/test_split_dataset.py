import sys
import os
import pandas as pd
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.split_dataset import read_csv_data, separate_features_and_target, save_data


@pytest.fixture
def sample_data():
    """Fixture for sample dataset used in tests."""
    data = pd.DataFrame({
        "Feature1": [1, 2, 3, 4],
        "Feature2": [5, 6, 7, 8],
        "Outcome": [0, 1, 0, 1]
    })
    return data


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture for creating a temporary directory."""
    return tmp_path


def test_read_csv_data(temp_dir, sample_data):
    """
    Test the read_csv_data function to ensure it reads a CSV file correctly.
    - Both DataFrames have the same columns.
    - The data content matches.
    """
    file_path = os.path.join(temp_dir, "sample.csv")
    sample_data.to_csv(file_path, index=False)

    # Read data using the function
    result = read_csv_data(file_path)

    # Ensure columns match
    assert list(result.columns) == list(sample_data.columns), "Columns do not match"

    # Ensure content matches
    pd.testing.assert_frame_equal(result.reset_index(drop=True), sample_data)


def test_separate_features_and_target(sample_data):
    """
    Test the separate_features_and_target function:
    - Ensure features and target are correctly separated.
    - Verify the number of columns in features and target.
    - Ensure no target column exists in features.
    """
    X, y = separate_features_and_target(sample_data, "Outcome")

    # Check column count
    assert X.shape[1] == sample_data.shape[1] - 1, "Number of feature columns is incorrect"
    assert y.shape[1] == 1, "Number of target columns is incorrect"

    # Ensure no target column in features
    assert "Outcome" not in X.columns, "Target column exists in features"

    # Ensure data integrity
    assert X.shape[0] == y.shape[0], "Mismatch in row counts between features and target"
    pd.testing.assert_series_equal(y["Outcome"], sample_data["Outcome"])


def test_save_data(temp_dir, sample_data):
    """
    Test the save_data function:
    - Ensure the file is created.
    - Verify that the saved data matches the input DataFrame.
    """
    file_path = os.path.join(temp_dir, "saved_data.csv")

    # Save data using the function
    save_data(sample_data, file_path)

    # Verify file exists
    assert os.path.exists(file_path), "Saved file does not exist"

    # Verify content matches
    saved_data = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(saved_data, sample_data)


def test_integration_split_functions(temp_dir, sample_data):
    """
    Test the integration of all functions:
    - Save the sample data.
    - Read it back using read_csv_data.
    - Separate features and target using separate_features_and_target.
    - Save the resulting features and target using save_data.
    - Verify the entire process works as expected.
    """
    # Save sample data
    file_path = os.path.join(temp_dir, "sample.csv")
    save_data(sample_data, file_path)

    # Read data back
    data = read_csv_data(file_path)

    # Separate features and target
    X, y = separate_features_and_target(data, "Outcome")

    # Save separated data
    X_file = os.path.join(temp_dir, "X.csv")
    y_file = os.path.join(temp_dir, "y.csv")
    save_data(X, X_file)
    save_data(y, y_file)

    # Verify saved features
    saved_X = pd.read_csv(X_file)
    pd.testing.assert_frame_equal(saved_X, X)

    # Verify saved target
    saved_y = pd.read_csv(y_file)
    pd.testing.assert_frame_equal(saved_y, y)

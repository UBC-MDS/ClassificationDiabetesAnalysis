# test_save_csv_data.py
# author: Javier Martinez
# date: 2024-12-15

import os
import pandas as pd
import pytest
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.save_csv_data import save_csv_data

# Test setup
test_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
test_dir = "tests/test_csv_dir"
test_csv_path = os.path.join(test_dir, "test.csv")
invalid_csv_path = os.path.join(test_dir, "test.txt")
invalid_dir_path = "/invalid/test.csv"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Create test directory
    os.makedirs(test_dir, exist_ok=True)
    yield
    # Cleanup
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

# Test: Save valid DataFrame successfully
def test_save_csv_data_success():
    save_csv_data(test_df, test_csv_path)
    assert os.path.exists(test_csv_path)

    # Verify the contents of the saved file
    loaded_df = pd.read_csv(test_csv_path)
    pd.testing.assert_frame_equal(loaded_df, test_df)

# Test: Raise TypeError for invalid data type
def test_save_csv_data_type_error():
    with pytest.raises(TypeError, match="The `data` parameter must be a pandas DataFrame."):
        save_csv_data([1, 2, 3], test_csv_path)

# Test: Raise ValueError for invalid file extension
def test_save_csv_data_invalid_file_extension():
    with pytest.raises(ValueError, match="The `file_path` must end with '.csv'."):
        save_csv_data(test_df, invalid_csv_path)

# Test: Raise PermissionError for unwritable directory
def test_save_csv_data_permission_error():
    with pytest.raises(PermissionError, match="The directory '/invalid' is not writable."):
        save_csv_data(test_df, invalid_dir_path)


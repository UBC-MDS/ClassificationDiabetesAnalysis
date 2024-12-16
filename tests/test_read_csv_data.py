# test_read_csv_data.py
# author: Javier Martinez
# date: 2024-12-15

import pytest
import os
import pandas as pd
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_csv_data import read_csv_data

# Test setup
test_csv_path = 'tests/test_csv_data/test.csv'
test_invalid_csv_path = 'tests/test_csv_data/test.txt'
test_dir_path = 'tests/test_csv_data_dir'

# Setup test directory and files
if not os.path.exists('tests/test_csv_data'):
    os.makedirs('tests/test_csv_data')

# Create a valid CSV file for testing
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
df.to_csv(test_csv_path, index=False)

# Create a non-CSV file for testing
with open(test_invalid_csv_path, 'w') as f:
    f.write("This is not a CSV file.")

# Create a directory to test IsADirectoryError
if not os.path.exists(test_dir_path):
    os.makedirs(test_dir_path)

# Tests

# Test that a valid CSV file is read successfully
def test_read_csv_data_valid_file():
    data = read_csv_data(test_csv_path)
    assert isinstance(data, pd.DataFrame)
    assert list(data.columns) == ['col1', 'col2']
    assert data.shape == (2, 2)

# Test that FileNotFoundError is raised for a non-existent file
def test_read_csv_data_file_not_found():
    with pytest.raises(FileNotFoundError, match="The file at 'non_existent.csv' does not exist."):
        read_csv_data('non_existent.csv')

# Test that IsADirectoryError is raised for a directory path
def test_read_csv_data_is_directory():
    with pytest.raises(IsADirectoryError, match=f"The path '{test_dir_path}' points to a directory, not a file."):
        read_csv_data(test_dir_path)

# Test that ValueError is raised for a non-CSV file
def test_read_csv_data_invalid_file_type():
    with pytest.raises(ValueError, match=f"The file at '{test_invalid_csv_path}' is not a CSV file."):
        read_csv_data(test_invalid_csv_path)


# Clean up
@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    # Cleanup test files and directories
    if os.path.exists(test_csv_path):
        os.remove(test_csv_path)
    if os.path.exists(test_invalid_csv_path):
        os.remove(test_invalid_csv_path)
    if os.path.exists('tests/test_csv_data/invalid.csv'):
        os.remove('tests/test_csv_data/invalid.csv')
    if os.path.exists(test_dir_path):
        os.rmdir(test_dir_path)
    if os.path.exists('tests/test_csv_data'):
        # Remove all files in the directory before removing it
        for file in os.listdir('tests/test_csv_data'):
            os.remove(os.path.join('tests/test_csv_data', file))
        os.rmdir('tests/test_csv_data')


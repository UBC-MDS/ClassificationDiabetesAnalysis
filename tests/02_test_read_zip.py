# test_read_zip.py
# author: Jenny Zhang
# date: 2024-12-12

import pytest
import os
import shutil
import responses
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

# Test files setup

# setup empty directory for data files to be downloaded to
if not os.path.exists('tests/test_zip_data1'):
    os.makedirs('tests/test_zip_data1')

# setup directory that contains a file for data files to be downloaded to
if not os.path.exists('tests/test_zip_data2'):
    os.makedirs('tests/test_zip_data2')
with open('tests/test_zip_data2/test4.txt', 'w') as file:
    pass  # The 'pass' statement does nothing, creating an empty file

test_files_txt_csv = ['test1.txt', 'test2.csv']
test_files_subdir = ['test1.txt', 'test2.csv', 'subdir/test3.txt']
test_files_2txt_csv = ['test1.txt', 'test2.csv', 'test4.txt']

# URL for Case 1 (zip file containing 'test1.txt' and 'test2.csv')
url_txt_csv_zip = 'https://github.com/ttimbers/breast_cancer_predictor_py/raw/main/tests/files_txt_csv.zip'

# URL for Case 2 ('test1.txt', test2.csv and 'subdir/test2.txt')
url_txt_subdir_zip = 'https://github.com/ttimbers/breast_cancer_predictor_py/raw/main/tests/files_txt_subdir.zip'

# URL for Case 3 (empty zip file)
url_empty_zip = 'https://github.com/ttimbers/breast_cancer_predictor_py/raw/main/tests/empty.zip'

# mock non-existing URL
@pytest.fixture
def mock_response():
    # Mock a response with a non-200 status code
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, 'https://example.com', status=404)
        yield

# Tests

# test read_zip function can download and extract a zip file containing two files 
def test_read_zip_txt_csv():
    read_zip(url_txt_csv_zip, 'tests/test_zip_data1')
    # List of files you expect to find in the directory
    for file in test_files_txt_csv:
        file_path = os.path.join('tests/test_zip_data1', file)
        assert os.path.isfile(file_path)
    # clean up unzipped files
    for file in test_files_txt_csv:
        if os.path.exists(file):
            os.remove(file)

# test read_zip function can download and extract a zip file containing two files 
# and subdirectories containing files
def test_read_zip_subdir():
    read_zip(url_txt_subdir_zip, 'tests/test_zip_data1')
    # List of files you expect to find in the directory
    for file in test_files_subdir:
        file_path = os.path.join('tests/test_zip_data1', file)
        assert os.path.isfile(file_path)
    # clean up unzipped files
    for file in test_files_subdir:
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists('testss/test_zip_data1/subdir'):
        shutil.rmtree('testss/test_zip_data1/subdir')

# test read_zip function can download and extract a zip file containing two files 
# into a directory that already contains a file
def test_read_zip_2txt_csv():
    read_zip(url_txt_csv_zip, 'tests/test_zip_data2')
    # List of files you expect to find in the directory
    for file in test_files_2txt_csv:
        file_path = os.path.join('tests/test_zip_data2', file)
        assert os.path.isfile(file_path)
    # clean up unzipped files
    for file in test_files_txt_csv:
        if os.path.exists(file):
            os.remove(file)

# test read_zip function throws an error if the zip file 
# at the input URL is empty
def test_read_zip_empty_zip():
    with pytest.raises(ValueError, match='The ZIP file is empty.'):
        read_zip(url_empty_zip, 'tests/test_zip_data1')

# test read_zip function throws an error if the input URL is invalid 
def test_read_zip_error_on_invalid_url(mock_response):
    with pytest.raises(ValueError, match='The URL provided does not exist.'):
        read_zip('https://example.com', 'tests/test_zip_data1')

# test read_zip function throws an error if the URL is not a zip file
def test_read_zip_error_on_nonzip_url():
    with pytest.raises(ValueError, match='The URL provided does not point to a zip file.'):
        read_zip('https://github.com/', 'tests/test_zip_data1')

# test read_zip function throws an error 
# if the  directory path provided does not exist
def test_read_zip_error_on_missing_dir():
    with pytest.raises(ValueError, match='The directory provided does not exist.'):
        read_zip(url_txt_csv_zip, 'tests/test_zip_data3')
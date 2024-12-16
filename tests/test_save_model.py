# test_save_model.py
# author: Javier Martinez
# date: 2024-12-15

import os
import pytest
import pickle
import shutil
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.save_model import save_model

# Test setup
test_model = {"model": "test_model_data"}
test_dir = "tests/test_model_dir"
test_model_path = os.path.join(test_dir, "test_model.pkl")
invalid_dir = "/invalid/path/test_model.pkl"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown():
    # Create test directory
    os.makedirs(test_dir, exist_ok=True)
    yield
    # Cleanup
    if os.path.exists(test_model_path):
        os.remove(test_model_path)
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

# Test: Model is saved successfully
def test_save_model_success():
    save_model(test_model, test_model_path)
    assert os.path.exists(test_model_path)

    # Validate that the saved file can be loaded correctly
    with open(test_model_path, 'rb') as f:
        loaded_model = pickle.load(f)
    assert loaded_model == test_model

# Test: Model is saved in a newly created directory
def test_save_model_create_directory():
    new_dir = os.path.join(test_dir, "subdir")
    new_model_path = os.path.join(new_dir, "test_model.pkl")
    save_model(test_model, new_model_path)
    assert os.path.exists(new_model_path)

    # Validate saved model
    with open(new_model_path, 'rb') as f:
        loaded_model = pickle.load(f)
    assert loaded_model == test_model

    # Cleanup
    if os.path.exists(new_model_path):
        os.remove(new_model_path)
    if os.path.exists(new_dir):
        os.rmdir(new_dir)


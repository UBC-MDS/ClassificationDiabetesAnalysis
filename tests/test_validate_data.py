# tests/test_validate_diabetes_data.py
# author: Jessica Kuo
# date: 2024-12-11

import pytest
import os
import numpy as np
import pandas as pd
import pandera as pa
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_diabetes_data import validate_diabetes_data

# Valid data example
valid_data = pd.DataFrame({
    "Outcome": [0, 1, 0],
    "Pregnancies": [0, 15, 5],
    "Glucose": [100, 240, 150],
    "BloodPressure": [80, 180, 90],
    "SkinThickness": [20, 80, 40],
    "Insulin": [0, 800, 100],
    "BMI": [25.0, 65.0, 30.0],
    "DiabetesPedigreeFunction": [0.5, 2.5, 1.0],
    "Age": [18, 90, 50]
})

def test_valid_data():
    # Should pass without error
    df_validated = validate_diabetes_data(valid_data)
    pd.testing.assert_frame_equal(df_validated, valid_data)

def test_wrong_type_input():
    # Passing a numpy array instead of DataFrame should raise TypeError
    arr_data = valid_data.to_numpy()
    with pytest.raises(TypeError):
        validate_diabetes_data(arr_data)

def test_empty_dataframe():
    # An empty DataFrame should raise ValueError
    empty_df = pd.DataFrame()
    with pytest.raises(ValueError):
        validate_diabetes_data(empty_df)

def test_out_of_range_values():
    # Make a copy of valid data and modify one column to go out of range
    invalid_df = valid_data.copy()
    invalid_df.loc[0, "Glucose"] = 300  # out of allowed range (50 to 240)
    with pytest.raises(pa.errors.SchemaErrors):
        validate_diabetes_data(invalid_df)

def test_missing_column():
    # Drop a required column
    invalid_df = valid_data.copy().drop("Outcome", axis=1)
    with pytest.raises(pa.errors.SchemaErrors):
        validate_diabetes_data(invalid_df)

def test_invalid_category():
    # Invalid Outcome value
    invalid_df = valid_data.copy()
    invalid_df.loc[0, "Outcome"] = 2  # Allowed is only [0,1]
    with pytest.raises(pa.errors.SchemaErrors):
        validate_diabetes_data(invalid_df)

def test_duplicate_rows():
    # Add a duplicate row to valid data
    invalid_df = pd.concat([valid_data, valid_data.iloc[[0]]], ignore_index=True)
    with pytest.raises(pa.errors.SchemaErrors):
        validate_diabetes_data(invalid_df)

def test_empty_row():
    # Add a completely empty row
    invalid_df = pd.concat([valid_data, pd.DataFrame([[np.nan]*len(valid_data.columns)], 
                                                     columns=valid_data.columns)], ignore_index=True)
    with pytest.raises(pa.errors.SchemaErrors):
        validate_diabetes_data(invalid_df)

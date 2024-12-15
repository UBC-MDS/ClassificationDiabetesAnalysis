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
    "Pregnancies": [0, 5, np.nan],
    "Glucose": [70, np.nan, 240],
    "BloodPressure": [80, 120, np.nan], 
    "SkinThickness": [20, np.nan, 80],
    "Insulin": [np.nan, 250, 800],
    "BMI": [22.5, 35.1, np.nan],
    "DiabetesPedigreeFunction": [0.2, np.nan, 2.5],
    "Age": [25, np.nan, 90],
})

# Case: wrong type passed to function
valid_data_as_np = valid_data.copy().to_numpy()
def test_valid_data_type():
    with pytest.raises(TypeError):
        validate_diabetes_data(valid_data_as_np)

# Case: empty data frame
case_empty_data_frame = valid_data.copy().iloc[0:0]
def test_valid_data_empty_data_frame():
    with pytest.raises(ValueError):
        validate_diabetes_data(case_empty_data_frame)

# Setup list of invalid data cases 
invalid_data_cases = []

# Case: missing "Outcome" column
case_missing_outcome_col = valid_data.copy()
case_missing_outcome_col = case_missing_outcome_col.drop("Outcome", axis=1)  # drop Outcome column
invalid_data_cases.append((case_missing_outcome_col, "`Outcome` from DataFrameSchema"))

# Case: label in "Outcome" column with wrong value
case_wrong_outcome_value = valid_data.copy()
case_wrong_outcome_value.loc[0, "Outcome"] = 3  # Invalid outcome value
invalid_data_cases.append((case_wrong_outcome_value, "Check incorrect type for 'Outcome' values is missing or incorrect"))

# Case: missing numeric columns (one for each numeric column) where column is missing
numeric_columns = valid_data.columns
for col in numeric_columns:
    case_missing_col = valid_data.copy()
    case_missing_col = case_missing_col.drop(col, axis=1)  # drop column
    invalid_data_cases.append((case_missing_col, f"'{col}' is missing from DataFrameSchema"))

# Generate 30 cases (one for each numeric column) where data is out of range (too large)
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_too_big = valid_data.copy()
    case_too_big[col] = case_too_big[col] + 10  # Adding an arbitrary value to make it out of range
    invalid_data_cases.append((case_too_big, f"Check absent or incorrect for numeric values in '{col}' being too large"))

# Generate 30 cases (one for each numeric column) where data is out of range (too small)
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_too_small = valid_data.copy()
    case_too_small[col] = case_too_small[col] - 10  # Adding an arbitrary value to make it out of range
    invalid_data_cases.append((case_too_small, f"Check absent or incorrect for numeric values in '{col}' being too small"))

# Generate 30 cases (one for each numeric column) where data is the wrong type
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_wrong_type = valid_data.copy()
    case_wrong_type[col] = case_wrong_type[col].fillna(0.0).astype(int)  # convert from float to int
    invalid_data_cases.append((case_wrong_type, f"Check incorrect type for float values in '{col}' is missing or incorrect"))

# Case: duplicate observations
case_duplicate = valid_data.copy()
case_duplicate = pd.concat([case_duplicate, case_duplicate.iloc[[0], :]], ignore_index=True)
invalid_data_cases.append((case_duplicate, f"Check absent or incorrect for duplicate rows"))

# Case: entire missing observation
case_missing_obs = valid_data.copy()
nan_row = pd.DataFrame([[np.nan] * (case_missing_obs.shape[1])], columns=case_missing_obs.columns)
case_missing_obs = pd.concat([case_missing_obs, nan_row], ignore_index=True)
invalid_data_cases.append((case_missing_obs, f"Check absent or incorrect for missing observations (e.g., a row of all missing values)"))

# Parameterize invalid data test cases
@pytest.mark.parametrize("invalid_data, description", invalid_data_cases)
def test_valid_w_invalid_data(invalid_data, description):
    with pytest.raises(pa.errors.SchemaErrors):
        validate_diabetes_data(invalid_data)

# test_data_deepchecks.py
# author: Jenny Zhang
# date: 2024-12-12

import pytest
import os
import sys
import numpy as np
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_deepchecks import data_deepchecks

# Sample valid data for testing
valid_data = pd.DataFrame({
    'Pregnancies': [6, 1, 8, 3, 5],
    'Glucose': [148, 85, 183, 120, 160],
    'BloodPressure': [72, 66, 64, 80, 110],
    'SkinThickness': [35, 29, 0, 20, 25],
    'Insulin': [0, 0, 0, 130, 400],
    'BMI': [33.6, 26.6, 23.3, 29.5, 31.2],
    'DiabetesPedigreeFunction': [0.627, 0.351, 0.672, 0.500, 0.250],
    'Age': [50, 31, 32, 45, 60],
    'Outcome': [1, 0, 1, 0, 1]
})

# Setup for invalid cases
invalid_data_cases = []

# Case: Class imbalance exceeds threshold (e.g., all Outcome values are 1)
case_imbalanced = valid_data.copy()
case_imbalanced['Outcome'] = [1, 1, 1, 1, 1]
invalid_data_cases.append((case_imbalanced, "Class imbalance exceeds threshold."))

# Case: Generate 9 cases (one for each numeric column) where data exceeds 5% null threshold
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_null = valid_data.copy()
    case_null[col] = np.nan
    invalid_data_cases.append((case_null, f"Null values in '{col}' exceed acceptable percentage."))

# Case: Generate 9 cases (one for each numeric column) where data exceeds outliers threshold
numeric_columns = valid_data.select_dtypes(include=np.number).columns
for col in numeric_columns:
    case_outlier = valid_data.copy()
    outliers = case_outlier[col].sample(n=2, random_state=123) 
    case_outlier.loc[outliers.index, col] = outliers * 10
    invalid_data_cases.append((case_outlier, f"Outliers detected in '{col}' beyond acceptable threshold."))

# Case: Duplicate rows
case_duplicate = valid_data.copy()
case_duplicate = pd.concat([case_duplicate, case_duplicate.iloc[[0], :]], ignore_index=True)
invalid_data_cases.append((case_duplicate, "Duplicate rows detected"))

# Case: Generate 8 cases (one for each numeric feature) where data's feature-label correlation exceeds threshold
for col in numeric_columns:
        if col != 'Outcome':  # Skip the label column
            # Create a strong correlation by setting the feature values based on 'Outcome'
            case_corr_feat_label = valid_data.copy()
            case_corr_feat_label[col] = case_corr_feat_label['Outcome'] * 100  # Create strong correlation
            invalid_data_cases.append((case_corr_feat_label, f"Feature-label correlation exceeds threshold for '{col}'"))

# Case: Generate 28 cases (8 * 7 / 2 unique pairs of features) where data's Feature-feature correlation exceeds threshold
numeric_feats = [col for col in numeric_columns if col != 'Outcome']
for col in numeric_feats:
    for i, col1 in enumerate(numeric_feats):
        for col2 in numeric_feats[i+1:]:  # Check each pair once
            # Create a strong correlation by setting one feature based on the other
            case_corr_feat_feat = valid_data.copy()
            case_corr_feat_feat[col2] = case_corr_feat_feat[col1] * 0.5
            invalid_data_cases.append((case_corr_feat_feat, f"Feature-feature correlation exceeds threshold between '{col1}' and '{col2}'"))

# Parameterize the invalid data tests
@pytest.mark.parametrize("invalid_data, description", invalid_data_cases)
def test_invalid_data_cases(invalid_data, description):
    with pytest.raises(ValueError, match=description):
        data_deepchecks(invalid_data)

# Success test: Valid data should pass without errors
def test_valid_data():
    # Valid data should pass the deepchecks without raising any errors
    try:
        data_deepchecks(valid_data)
    except ValueError as e:
        pytest.fail(f"Valid data raised an error: {e}")

# Edge case: Generate 9 cases (one for each numeric column) where mixed data types are in dangerous zone **Testing for warnings**
warning_data_cases = []
for col in numeric_columns:
    case_mixed_dtype = valid_data.copy()
    num_rare_values = int(len(case_mixed_dtype) * 0.2)
    rare_indices = np.random.choice(case_mixed_dtype.index, num_rare_values, replace=False)
    case_mixed_dtype.loc[rare_indices, col] = 'string'
    warning_data_cases.append((case_mixed_dtype, "Rare data type in dangerous zone for '{col}'."))

@pytest.mark.parametrize("warning_data, description", warning_data_cases)
def test_mixed_dtype_warning():
    # Warning should be raised as rare data type is in dangerous zone of 1% to 20%
    with pytest.warns(UserWarning, match=description):
        data_deepchecks(warning_data)
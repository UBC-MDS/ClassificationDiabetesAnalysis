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

# Generate a larger dataset with 100 samples
np.random.seed(123)  # For reproducibility
valid_data = pd.DataFrame({
    'Pregnancies': np.random.randint(0, 15, size=100),
    'Glucose': np.random.randint(50, 240, size=100),
    'BloodPressure': np.random.randint(40, 180, size=100),
    'SkinThickness': np.random.randint(0, 80, size=100),
    'Insulin': np.random.randint(0, 800, size=100),
    'BMI': np.random.uniform(0, 65, size=100),
    'DiabetesPedigreeFunction': np.random.uniform(0, 2.5, size=100),
    'Age': np.random.randint(18, 90, size=100),
    'Outcome': np.random.choice([0, 1], size=100)
})

# Setup for invalid cases
invalid_data_cases = []

# Retrieve number of numeric columns and numeric features
numeric_columns = valid_data.select_dtypes(include=np.number).columns
numeric_feats = [col for col in numeric_columns if col != 'Outcome']

# Case: Class imbalance exceeds threshold (e.g., all Outcome values are 1)
case_imbalanced = valid_data.copy()
num_imbalanced = int(len(valid_data) * 0.8)
case_imbalanced['Outcome'] = [1] * num_imbalanced + [0] * (len(valid_data) - num_imbalanced)
invalid_data_cases.append((case_imbalanced, "Class imbalance exceeds the maximum acceptable threshold."))

# Case: Generate 8 cases (one for each numeric features) where data exceeds 5% null threshold
for col in numeric_feats:
    case_null = valid_data.copy()
    case_null[col] = np.nan
    invalid_data_cases.append((case_null, "Percent of nulls exceeds the maximum acceptable threshold for at least one column."))

# Case: Generate 9 cases (one for each numeric features) where data exceeds outliers threshold
for col in numeric_feats:
    case_outlier = valid_data.copy()
    outliers_count = int(len(case_outlier) * 0.3)
    outliers = case_outlier[col].sample(n=outliers_count, random_state=123) 
    case_outlier.loc[outliers.index, col] = outliers * 10
    invalid_data_cases.append((case_outlier, "Number of outlier samples exceeds the maximum acceptable threshold."))

# Case: Duplicate rows
case_duplicate = valid_data.copy()
case_duplicate = pd.concat([case_duplicate, case_duplicate.iloc[[0], :]], ignore_index=True)
invalid_data_cases.append((case_duplicate, "Data duplicates exceed the maximum acceptable threshold."))

# Case: Generate 8 cases (one for each numeric features) where data's feature-label correlation exceeds threshold
for col in numeric_columns:
        if col != 'Outcome':  # Skip the label column
            # Create a strong correlation by setting the feature values based on 'Outcome'
            case_corr_feat_label = valid_data.copy()
            case_corr_feat_label[col] = case_corr_feat_label['Outcome'] * 100  # Create strong correlation
            invalid_data_cases.append((case_corr_feat_label, "Feature-Label correlation exceeds the maximum acceptable threshold."))

# Case: Generate 28 cases (8 * 7 / 2 unique pairs of features) where data's Feature-feature correlation exceeds threshold
for col in numeric_feats:
    for i, col1 in enumerate(numeric_feats):
        for col2 in numeric_feats[i+1:]:  # Check each pair once
            # Create a strong correlation by setting one feature based on the other
            case_corr_feat_feat = valid_data.copy()
            case_corr_feat_feat[col2] = case_corr_feat_feat[col1] * 0.5
            invalid_data_cases.append((case_corr_feat_feat, "Feature-feature correlation exceeds the maximum acceptable threshold."))

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

# Edge case: Generate 9 cases (one for each numeric features) where mixed data types are in dangerous zone **Testing for warnings**
warning_data_cases = []
for col in numeric_feats:
    case_mixed_dtype = valid_data.copy()
    num_rare_values = int(len(case_mixed_dtype) * 0.1)
    rare_indices = np.random.choice(case_mixed_dtype.index, num_rare_values, replace=False)
    case_mixed_dtype.loc[rare_indices, col] = 'string'
    warning_data_cases.append((case_mixed_dtype, "Percentage of rare data type in dangerous zone for at least one column"))

@pytest.mark.parametrize("warning_data, description", warning_data_cases)
def test_mixed_dtype_warning(warning_data, description):
    # Warning should be raised as rare data type is in dangerous zone of 1% to 20%
    with pytest.warns(UserWarning, match=description):
        data_deepchecks(warning_data)
import pandas as pd
import warnings
from deepchecks.tabular import Dataset
from deepchecks.tabular.checks import (
    ClassImbalance, 
    PercentOfNulls,
    OutlierSampleDetection,
    DataDuplicates,
    MixedDataTypes,
    FeatureLabelCorrelation, 
    FeatureFeatureCorrelation
)
from deepchecks.tabular.checks.data_integrity import PercentOfNulls


def data_deepchecks(diabetes_train_dataframe):
    """
    Perform various deep checks on the training dataset to validate its quality. 

    This function checks the following conditions on the training data:
    1. Class imbalance for the target variable ('Outcome').
    2. Percent of missing (null) values in the data.
    3. Outlier samples based on the loOP algorithm.
    4. Presence of duplicate data points.
    5. Mixed data types across columns.
    6. Correlations between the target variable and features, as well as between features.

    Parameters
    ----------
    diabetes_train_dataframe : pandas.DataFrame
        The DataFrame containing diabetes-related training data, which includes columns such as 'Pregnancies', 'Glucose', 
        'BloodPressure', and other related measurements. The data is validated based on specific criteria for 
        each column.

    Returns
    -------
    None

    Raises
    -------
        ValueError: If any of the following conditions are not met:
            - Class imbalance exceeds the maximum threshold.
            - Percent of nulls exceeds the threshold.
            - Outlier ratio exceeds the threshold.
            - Data duplicates exceed the threshold.
            - Correlations between the target variable and features or between features exceed thresholds.
        Warning: If the percentage of rare data types in any column is in a dangerous zone (less than 1% or greater than 20%).
    """

    ## Deepchecks - data related
    # validate training data for class imbalance for target variable 
    # Do these on training data as part of EDA! 
    diabetes_train_ds = Dataset(diabetes_train_dataframe, label = 'Outcome', cat_features=[])

    check_lab_cls_imb = ClassImbalance().add_condition_class_ratio_less_than(0.4)
    check_lab_cls_imb_result = check_lab_cls_imb.run(dataset = diabetes_train_ds)

    if check_lab_cls_imb_result.passed_conditions():
        raise ValueError("Class imbalance exceeds the maximum acceptable threshold.")
    
    # validate training data for percent of nulls
    check_pct_nulls = PercentOfNulls().add_condition_percent_of_nulls_not_greater_than(0.05)
    check_pct_nulls_result = check_pct_nulls.run(dataset = diabetes_train_ds)

    if not check_pct_nulls_result.passed_conditions():
        raise ValueError("Percent of nulls exceeds the maximum acceptable threshold for at least one column.")
    
    # validate training data for percent of outlier samples using loOP algo
    check_out_sample = (
        OutlierSampleDetection(nearest_neighbors_percent = 0.01, extent_parameter = 3)
        .add_condition_outlier_ratio_less_or_equal(max_outliers_ratio = 0.001, outlier_score_threshold = 0.9)
    )
    check_out_sample_result = check_out_sample.run(dataset = diabetes_train_ds)

    if not check_out_sample_result.passed_conditions():
        raise ValueError("Number of outlier samples exceeds the maximum acceptable threshold.")
    
    # validate training data for data duplicates
    # set duplicate condition to 0 as would not expect any two patient with the exact same situation
    check_data_dup = DataDuplicates().add_condition_ratio_less_or_equal(0)
    check_data_dup_result = check_data_dup.run(dataset = diabetes_train_ds)

    if not check_data_dup_result.passed_conditions():
        raise ValueError("Data duplicates exceed the maximum acceptable threshold.")
    
    # validate training data for mixed data types across all columns
    check_mix_dtype = MixedDataTypes().add_condition_rare_type_ratio_not_in_range((0.01, 0.2))
    check_mix_dtype_result = check_mix_dtype.run(dataset = diabetes_train_ds)

    if not check_mix_dtype_result.passed_conditions():
        # raise a warning instead of an error in this case
        warnings.warn("Percentage of rare data type in dangerous zone for at least one column")

    ## Deepchecks - correlation
    # validate training data for anomalous correlations between target/response variable 
    # and features/explanatory variables, 
    # as well as anomalous correlations between features/explanatory variables

    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.7)
    check_feat_lab_corr_result = check_feat_lab_corr.run(dataset = diabetes_train_ds)

    check_feat_feat_corr = FeatureFeatureCorrelation().add_condition_max_number_of_pairs_above_threshold(threshold = 0.7, n_pairs = 0)
    check_feat_feat_corr_result = check_feat_feat_corr.run(dataset = diabetes_train_ds)

    if not check_feat_lab_corr_result.passed_conditions():
        raise ValueError("Feature-Label correlation exceeds the maximum acceptable threshold.")

    if not check_feat_feat_corr_result.passed_conditions():
        raise ValueError("Feature-feature correlation exceeds the maximum acceptable threshold.")

    


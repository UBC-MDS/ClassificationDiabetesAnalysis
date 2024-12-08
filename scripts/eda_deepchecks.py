# eda_deepchecks.py
# author: Jenny Zhang
# date: 2024-12-03

import click
import os

import altair as alt
import altair_ally as aly

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

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
import warnings


@click.command()
@click.option('--validated-data', type=str, help="Path to validated data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
def main(validated_data, data_to, plot_to):
    '''This script splits the raw data into train and test sets,
    Plots the densities of each feature, correlation heatmap between features, 
    and pairwise scatterplot in the training data by outcome
    and displays them as a grid of plots. Also saves the plots.'''

    df = pd.read_csv(validated_data, index_col = 0)

    # EDA
    # print(df_original.shape)
    print(df.shape)

    df.info()

    # Create the split
    train_df, test_df = train_test_split(df,
                                         train_size = 0.7, 
                                         random_state=123)
    
    train_df.to_csv(os.path.join(data_to, "train_df.csv"))
    test_df.to_csv(os.path.join(data_to, "test_df.csv"))
    
    # Explore training data
    census_summary = train_df.describe()
    census_summary
    
    # List features
    features = census_summary.columns.tolist()
    features
    
    # Visualize feature distributions
    feature_histograms = alt.Chart(train_df).transform_calculate(
    ).mark_bar(opacity=0.5).encode( 
        x = alt.X(alt.repeat()).type('quantitative').bin(maxbins=30), 
        y= alt.Y('count()').stack(False),
        color = 'Outcome:N'
    ).properties( 
        height=250,
        width=250
    ).repeat(
        features, columns=2
    )
    
    feature_histograms.save(os.path.join(plot_to, 'feature_histograms.png'),
                            scale_factor=2.0)

    ## Deepchecks - data related
    # validate training data for class imbalance for target variable 
    # Do these on training data as part of EDA! 
    train_df_ds = Dataset(train_df, label = 'Outcome', cat_features=[])

    check_lab_cls_imb = ClassImbalance().add_condition_class_ratio_less_than(0.4)
    check_lab_cls_imb_result = check_lab_cls_imb.run(dataset = train_df_ds)

    if check_lab_cls_imb_result.passed_conditions():
        raise ValueError("Class imbalance exceeds the maximum acceptable threshold.")
    
    # validate training data for percent of nulls
    check_pct_nulls = PercentOfNulls().add_condition_percent_of_nulls_not_greater_than(0.05)
    check_pct_nulls_result = check_pct_nulls.run(dataset = train_df_ds)

    if not check_pct_nulls_result.passed_conditions():
        raise ValueError("Percent of nulls exceeds the maximum acceptable threshold for at least one column.")
    
    # validate training data for percent of outlier samples using loOP algo
    check_out_sample = (
        OutlierSampleDetection(nearest_neighbors_percent = 0.01, extent_parameter = 3)
        .add_condition_outlier_ratio_less_or_equal(max_outliers_ratio = 0.001, outlier_score_threshold = 0.9)
    )
    check_out_sample_result = check_out_sample.run(dataset = train_df_ds)

    if not check_out_sample_result.passed_conditions():
        raise ValueError("Number of outlier samples exceeds the maximum acceptable threshold.")
    
    # validate training data for data duplicates
    # set duplicate condition to 0 as would not expect any two patient with the exact same situation
    check_data_dup = DataDuplicates().add_condition_ratio_less_or_equal(0)
    check_data_dup_result = check_data_dup.run(dataset = train_df_ds)

    if not check_data_dup_result.passed_conditions():
        raise ValueError("Data duplicates exceed the maximum acceptable threshold.")
    
    # validate training data for mixed data types across all columns
    check_mix_dtype = MixedDataTypes().add_condition_rare_type_ratio_not_in_range((0.01, 0.2))
    check_mix_dtype_result = check_mix_dtype.run(dataset = train_df_ds)

    if not check_mix_dtype_result.passed_conditions():
        # raise a warning instead of an error in this case
        warnings.warn("Percentage of rare data type in dangerous zone for at least one column")
    

    # Visualize correlations across features
    corr_plot = aly.corr(train_df)

    corr_plot.save(os.path.join(plot_to, 'correlation_heat_map.png'),
                   scale_factor=2.0)

    
    # Visualize relationships
    scatter_plot = aly.pair(train_df[features].sample(300), color='Outcome:N')

    scatter_plot.save(os.path.join(plot_to, 'pairwise_scatterplot.png'), 
                      scale_factor=2.0)
    
    ## Deepchecks - correlation
    # validate training data for anomalous correlations between target/response variable 
    # and features/explanatory variables, 
    # as well as anomalous correlations between features/explanatory variables

    check_feat_lab_corr = FeatureLabelCorrelation().add_condition_feature_pps_less_than(0.7)
    check_feat_lab_corr_result = check_feat_lab_corr.run(dataset = train_df_ds)

    check_feat_feat_corr = FeatureFeatureCorrelation().add_condition_max_number_of_pairs_above_threshold(threshold = 0.7, n_pairs = 0)
    check_feat_feat_corr_result = check_feat_feat_corr.run(dataset = train_df_ds)

    if not check_feat_lab_corr_result.passed_conditions():
        raise ValueError("Feature-Label correlation exceeds the maximum acceptable threshold.")

    if not check_feat_feat_corr_result.passed_conditions():
        raise ValueError("Feature-feature correlation exceeds the maximum acceptable threshold.")

if __name__ == '__main__':
    main()
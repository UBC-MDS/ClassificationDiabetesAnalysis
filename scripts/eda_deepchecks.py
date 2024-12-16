# eda_deepchecks.py
# author: Jenny Zhang
# date: 2024-12-03

# Usage: 
# python scripts/eda_deepchecks.py \
#     --validated-data=data/processed/diabetes_validated.csv \
#     --data-to=data/processed \
#     --plot-to=results/figures

import click
import os
import sys
import pandas as pd

import altair as alt
import altair_ally as aly

from sklearn.model_selection import train_test_split

import warnings
for warning_type in [FutureWarning, DeprecationWarning]:
    warnings.filterwarnings("ignore", category=warning_type)
# warnings.filterwarnings("ignore", category=DeprecationWarning)
# warnings.filterwarnings("ignore", category=FutureWarning)

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.data_deepchecks import data_deepchecks


@click.command()
@click.option('--validated-data', type=str, help="Path to validated data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
@click.option('--plot-to', type=str, help="Path to directory where the plot will be written to")
def main(validated_data, data_to, plot_to):
    '''This script splits the raw data into train and test sets,
    Plots the densities of each feature, correlation heatmap between features, 
    and pairwise scatterplot in the training data by outcome
    and displays them as a grid of plots. Also saves the plots.'''

    diabetes_validated = pd.read_csv(validated_data, index_col = 0)

    # EDA
    # print(diabetes.shape)
    diabetes_validated.shape

    diabetes_validated.info()

    # Create the split
    diabetes_train, diabetes_test = train_test_split(diabetes_validated,
                                         train_size = 0.7, 
                                         random_state = 123)
    
    diabetes_train.to_csv(os.path.join(data_to, "diabetes_train.csv"))
    diabetes_test.to_csv(os.path.join(data_to, "diabetes_test.csv"))
    
    # Explore training data
    census_summary = diabetes_train.describe()
    census_summary
    
    # List features
    features = census_summary.columns.tolist()
    features

    # Conduct deepchecks
    data_deepchecks(diabetes_train)
    
    # Visualize feature distributions
    feature_histograms = alt.Chart(diabetes_train).transform_calculate(
    ).mark_bar(opacity=0.5).encode( 
        x = alt.X(alt.repeat()).type('quantitative').bin(maxbins=30), 
        y= alt.Y('count()').stack(False),
        color = 'Outcome:N'
    ).properties( 
        height=250,
        width=250
    ).repeat(
        features, 
        columns=3
    )
    
    feature_histograms.save(os.path.join(plot_to, 'feature_histograms.png'),
                            scale_factor=2.0)

    # Visualize correlations across features
    corr_plot = aly.corr(diabetes_train)

    corr_plot.save(os.path.join(plot_to, 'correlation_heatmap.png'),
                   scale_factor=2.0)

    
    # Visualize relationships
    scatter_plot = aly.pair(diabetes_train[features].sample(300), color='Outcome:N')

    scatter_plot.save(os.path.join(plot_to, 'pairwise_scatterplot.png'), 
                      scale_factor=2.0)
 
if __name__ == '__main__':
    main()
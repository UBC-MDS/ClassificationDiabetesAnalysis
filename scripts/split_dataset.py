# split_dataset.py
# author: Javier Martinez
# date: 2024-12-05

# Usage: 
# python scripts/split_dataset.py \
#     --train-file ./data/processed/diabetes_train.csv \
#     --test-file ./data/processed/diabetes_test.csv \
#     --output-dir ./data/processed

import os
import pandas as pd
import click
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_csv_data import read_csv_data
from src.save_csv_data import save_csv_data


@click.command()
@click.option('--train-file', type=str, default="../data/processed/diabetes_train.csv", help="Path to the processed diabetes_train CSV file")
@click.option('--test-file', type=str, default="../data/processed/diabetes_test.csv", help="Path to the processed diabetes_test CSV file")
@click.option('--output-dir', type=str, default="../data/processed/", help="Path to the directory where split data will be saved")
def main(train_file, test_file, output_dir):
    """
    Processes separate train and test datasets, separates features and target variable, 
    and saves them as separate CSV files.

    Parameters:
    -----------
    train_file : str
        Path to the input CSV file containing the processed training dataset.
    test_file : str
        Path to the input CSV file containing the processed testing dataset.
    output_dir : str
        Directory where the resulting split datasets (X_train, y_train, X_test, y_test) will be saved.
    """
    # Load the processed datasets
    diabetes_train = pd.read_csv(train_file, index_col = 0)
    diabetes_test = pd.read_csv(test_file, index_col = 0)

    # Separate features and target variable for train set
    X_train = diabetes_train.drop(columns=['Outcome'])
    y_train = diabetes_train[['Outcome']]

    # Separate features and target variable for test set
    X_test = diabetes_test.drop(columns=['Outcome'])
    y_test = diabetes_test[['Outcome']]

    # Save the split data as CSV files
    save_csv_data(X_train, os.path.join(output_dir, 'X_train.csv'))
    save_csv_data(y_train, os.path.join(output_dir, 'y_train.csv'))
    save_csv_data(X_test, os.path.join(output_dir, 'X_test.csv'))
    save_csv_data(y_test, os.path.join(output_dir, 'y_test.csv'))


if __name__ == '__main__':
    main()

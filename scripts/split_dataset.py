# split_dataset.py
# author: Javier Martinez
# date: 2024-12-05

import os
import pandas as pd
import click
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_csv_data import read_csv_data
from src.save_csv_data import save_csv_data


@click.command()
@click.option('--train-file', type=str, default="../data/processed/train_df.csv", help="Path to the processed train_df CSV file")
@click.option('--test-file', type=str, default="../data/processed/test_df.csv", help="Path to the processed test_df CSV file")
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
    train_df = read_csv_data(train_file)
    test_df = read_csv_data(test_file)

    # Separate features and target variable for train set
    X_train = train_df.drop(columns=['Outcome'])
    y_train = train_df[['Outcome']]

    # Separate features and target variable for test set
    X_test = test_df.drop(columns=['Outcome'])
    y_test = test_df[['Outcome']]

    # Save the split data as CSV files
    save_csv_data(X_train, os.path.join(output_dir, 'X_train.csv'))
    save_csv_data(y_train, os.path.join(output_dir, 'y_train.csv'))
    save_csv_data(X_test, os.path.join(output_dir, 'X_test.csv'))
    save_csv_data(y_test, os.path.join(output_dir, 'y_test.csv'))


if __name__ == '__main__':
    main()

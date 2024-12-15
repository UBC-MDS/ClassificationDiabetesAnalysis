# split_dataset.py
# author: Javier Martinez
# date: 2024-12-05

import os
import pandas as pd
import click


def read_csv_data(file_path):
    """
    Reads a CSV file and loads it into a pandas DataFrame.

    Parameters:
    -----------
    file_path : str
        Path to the CSV file.

    Returns:
    --------
    pd.DataFrame
        A pandas DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(file_path)


def separate_features_and_target(data, target_column):
    """
    Separates features and target variable from the dataset.

    Parameters:
    -----------
    data : pd.DataFrame
        The dataset containing features and target variable.
    target_column : str
        Name of the column representing the target variable.

    Returns:
    --------
    tuple
        A tuple containing:
        - X (pd.DataFrame): Features DataFrame.
        - y (pd.DataFrame): Target variable DataFrame.
    """
    X = data.drop(columns=[target_column])
    y = data[[target_column]]
    return X, y


def save_data(data, file_path):
    """
    Saves a pandas DataFrame to a CSV file.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to be saved.
    file_path : str
        Path to save the CSV file.
    """
    data.to_csv(file_path, index=False)


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
    os.makedirs(output_dir, exist_ok=True)

    # Load the processed datasets
    train_df = read_csv_data(train_file)
    test_df = read_csv_data(test_file)

    # Separate features and target variable for train and test sets
    X_train, y_train = separate_features_and_target(train_df, 'Outcome')
    X_test, y_test = separate_features_and_target(test_df, 'Outcome')

    # Save the split data as CSV files
    save_data(X_train, os.path.join(output_dir, 'X_train.csv'))
    save_data(y_train, os.path.join(output_dir, 'y_train.csv'))
    save_data(X_test, os.path.join(output_dir, 'X_test.csv'))
    save_data(y_test, os.path.join(output_dir, 'y_test.csv'))


if __name__ == '__main__':
    main()

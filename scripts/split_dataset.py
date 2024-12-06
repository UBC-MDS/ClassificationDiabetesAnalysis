# split_dataset.py
# author: Javier Martinez
# date: 2024-12-05

import os
import pandas as pd
from sklearn.model_selection import train_test_split
import click


@click.command()
@click.option('--input-file', type=str, default="../data/processed/train_df.csv", help="Path to the processed train_df CSV file")
@click.option('--output-dir', type=str, default="../data/processed/", help="Path to the directory where split data will be saved")
def main(input_file, output_dir):
    """
    Splits a dataset into training and testing sets and saves the results as separate CSV files.

    Parameters:
    -----------
    input_file : str
        Path to the input CSV file containing the processed dataset.
    output_dir : str
        Directory where the resulting split datasets (X_train, y_train, X_test, y_test) will be saved.

    Outputs:
    --------
    Four CSV files saved in the specified output directory:
    - X_train.csv: Features for the training set.
    - y_train.csv: Labels for the training set.
    - X_test.csv: Features for the testing set.
    - y_test.csv: Labels for the testing set.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load the processed dataset
    train_df = pd.read_csv(input_file)

    # Split the data into training and testing sets
    train_set, test_set = train_test_split(train_df, test_size=0.2, random_state=123, stratify=train_df['Outcome'])

    # Separate features and target variable for train and test sets
    X_train = train_set.drop(columns=['Outcome'])
    y_train = train_set[['Outcome']]
    X_test = test_set.drop(columns=['Outcome'])
    y_test = test_set[['Outcome']]

    # Save the split data as CSV files
    X_train.to_csv(os.path.join(output_dir, 'X_train.csv'), index=False)
    y_train.to_csv(os.path.join(output_dir, 'y_train.csv'), index=False)
    X_test.to_csv(os.path.join(output_dir, 'X_test.csv'), index=False)
    y_test.to_csv(os.path.join(output_dir, 'y_test.csv'), index=False)


if __name__ == '__main__':
    main()

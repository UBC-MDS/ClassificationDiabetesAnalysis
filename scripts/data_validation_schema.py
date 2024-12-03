# data_validation_schema.py
# author: Jenny Zhang
# date: 2024-12-03

import click
import os
import numpy as np
import pandas as pd
import pandera as pa


@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
def main(raw_data, data_to):
    '''This script runs through schema data validation checks, 
    and then preprocesses the data to be used in exploratory data analysis.'''

    # load data
    df_original = pd.read_csv(raw_data)

    # validate data
    # Configure logging
    logging.basicConfig(
        filename="validation_errors.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO,
    )

    # Define schema
    schema = pa.DataFrameSchema(
        { 
            "Outcome": pa.Column(int, pa.Check.isin([0, 1])),
            "Pregnancies": pa.Column(int, pa.Check.between(0, 15), nullable=True),
            "Glucose": pa.Column(int, pa.Check.between(50, 240), nullable=True),
            "BloodPressure": pa.Column(int, pa.Check.between(40, 180), nullable=True),
            "SkinThickness": pa.Column(int, pa.Check.between(0, 80), nullable=True),
            "Insulin": pa.Column(int, pa.Check.between(0, 800), nullable=True),
            "BMI": pa.Column(float, pa.Check.between(0, 65), nullable=True),
            "DiabetesPedigreeFunction": pa.Column(float, pa.Check.between(0, 2.5), nullable=True),
            "Age": pa.Column(int, pa.Check.between(18, 90), nullable=True),
        },
        checks=[
            pa.Check(lambda df: ~df.duplicated().any(), error="Duplicate rows found."),
            pa.Check(lambda df: ~(df.isna().all(axis=1)).any(), error="Empty rows found.")
        ],
        drop_invalid_rows=False,  # Ensure this is properly closed
    )

    # Initialize error cases DataFrame
    error_cases = pd.DataFrame()
    data = df_original.copy()

    # Validate data and handle errors
    try:
        validated_data = schema.validate(data, lazy=True)
    except pa.errors.SchemaErrors as e:
        error_cases = e.failure_cases

        # Convert the error message to a JSON string
        error_message = json.dumps(e.message, indent=2)
        logging.error("\n" + error_message)

    # Filter out invalid rows based on the error cases
    if not error_cases.empty:
        invalid_indices = error_cases["index"].dropna().unique()
        df = (
            data.drop(index=invalid_indices)
            .reset_index(drop=True)
            .drop_duplicates()
            .dropna(how="all")
        )
    else:
        df = data
    
    # save processed 
    df.to_csv(os.path.join(data_to, "df.csv"))

if __name__ == '__main__':
    main()
# data_validation_schema.py
# author: Jenny Zhang
# date: 2024-12-03

# Usage:
# python scripts/data_validation_schema.py \
#     --raw-data=data/raw/diabetes.csv \
#     --data-to=data/processed

import click
import os
import sys
import pandas as pd
import pandera as pa
import json
import logging
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.validate_diabetes_data import validate_diabetes_data

@click.command()
@click.option('--raw-data', type=str, help="Path to raw data")
@click.option('--data-to', type=str, help="Path to directory where processed data will be written to")
def main(raw_data, data_to):
    '''This script runs through schema data validation checks, 
    and then preprocesses the data to be used in exploratory data analysis.'''

    # load data
    diabetes_original = pd.read_csv(raw_data)

    # validate data
    # Configure logging
    logging.basicConfig(
        filename="validation_errors.log",
        filemode="w",
        format="%(asctime)s - %(message)s",
        level=logging.INFO,
    )

    # Initialize error cases DataFrame
    error_cases = pd.DataFrame()
    data = diabetes_original.copy()

   # Validate data and handle errors
    try:
        validated_data = validate_diabetes_data(data)
    except pa.errors.SchemaErrors as e:
        error_cases = e.failure_cases

        # Convert the error message to a JSON string
        error_message = json.dumps(e.message, indent=2)
        logging.error("\n" + error_message)

    # Filter out invalid rows based on the error cases
    if not error_cases.empty:
        invalid_indices = error_cases["index"].dropna().unique()
        diabetes_validated = (
            data.drop(index=invalid_indices)
            .reset_index(drop=True)
            .drop_duplicates()
            .dropna(how="all")
        )
    else:
        diabetes_validated = data
    
    # save processed 
    diabetes_validated.to_csv(os.path.join(data_to, "diabetes_validated.csv"))

if __name__ == '__main__':
    main()
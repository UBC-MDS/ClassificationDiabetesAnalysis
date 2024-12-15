# src/validate_diabetes_data.py
# author: Jessica Kuo
# date: 2024-12-11

import pandas as pd
import pandera as pa

def validate_diabetes_data(diabetes_dataframe):
    """
    Validates the input diabetes data in the form of a pandas DataFrame against a predefined schema,
    and returns the validated DataFrame.
    This function checks that the columns in the input DataFrame conform to the expected types and value ranges.
    It also ensures there are no duplicate rows and no entirely empty rows.
    Parameters
    ----------
    diabetes_dataframe : pandas.DataFrame
        The DataFrame containing diabetes-related data, which includes columns such as 'Outcome', 'Pregnancies',
        'Glucose', 'BloodPressure', etc. The data is validated based on specific criteria for each column.
    Returns
    -------
    pandas.DataFrame
        The validated DataFrame that conforms to the specified schema.
    Raises
    ------
    pandera.errors.SchemaError
        If the DataFrame does not conform to the specified schema (e.g., incorrect data types, out-of-range values,
        duplicate rows, or empty rows).
    Notes
    -----
    The following columns are validated:
        - 'Outcome': must be either 0 or 1.
        - 'Pregnancies': between 0 and 15, inclusive.
        - 'Glucose': between 50 and 240, inclusive.
        - 'BloodPressure': between 40 and 180, inclusive.
        - 'SkinThickness': between 0 and 80, inclusive.
        - 'Insulin': between 0 and 800, inclusive.
        - 'BMI': between 0 and 65, inclusive.
        - 'DiabetesPedigreeFunction': between 0 and 2.5, inclusive.
        - 'Age': between 18 and 90, inclusive.
        - Additionally, no duplicate rows and no completely empty rows are allowed.
    """
    if not isinstance(diabetes_dataframe, pd.DataFrame):
        raise TypeError("Input must be a pandas DataFrame")    
    if diabetes_dataframe.empty:
        raise ValueError("Dataframe must contain observations.")

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
        ]
    )

    # Validate the DataFrame. If it fails, pandera will raise a SchemaError.
    schema.validate(diabetes_dataframe, lazy=True)

    return diabetes_dataframe

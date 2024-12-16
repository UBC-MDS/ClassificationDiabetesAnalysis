import pandas as pd
import os

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

    Raises:
    -------
    FileNotFoundError
        If the file does not exist at the given path.
    IsADirectoryError
        If the file_path points to a directory instead of a file.
    ValueError
        If the file is not a CSV file.
    RuntimeError
        If an error occurs while reading the CSV file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file at '{file_path}' does not exist.")
    
    if os.path.isdir(file_path):
        raise IsADirectoryError(f"The path '{file_path}' points to a directory, not a file.")
    
    if not file_path.endswith('.csv'):
        raise ValueError(f"The file at '{file_path}' is not a CSV file. Please provide a valid CSV file.")
    
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the CSV file: {e}")

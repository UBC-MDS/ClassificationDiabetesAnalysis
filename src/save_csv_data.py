import pandas as pd
import os

def save_csv_data(data, file_path, index=False):
    """
    Saves a pandas DataFrame to a CSV file.

    Parameters:
    -----------
    data : pd.DataFrame
        The DataFrame to be saved.
    file_path : str
        Path to save the CSV file.
    index : bool, optional, default False
        Whether to write row names (indices). Defaults to False.

    Raises:
    -------
    TypeError
        If `data` is not a pandas DataFrame.
    ValueError
        If the file_path does not have a valid `.csv` extension.
    PermissionError
        If the program does not have permission to write to the specified path.
    IOError
        For any other I/O-related errors during file writing.
    """
    # Check if data is a pandas DataFrame
    if not isinstance(data, pd.DataFrame):
        raise TypeError("The `data` parameter must be a pandas DataFrame.")
    
    # Check if file_path ends with '.csv'
    if not file_path.endswith('.csv'):
        raise ValueError("The `file_path` must end with '.csv'. Please provide a valid file name.")
    
    # Check if the directory is writable
    directory = os.path.dirname(file_path)
    if directory and not os.access(directory, os.W_OK):
        raise PermissionError(f"The directory '{directory}' is not writable.")
    
    try:
        # Attempt to save the DataFrame
        data.to_csv(file_path, index=index)
    except PermissionError as e:
        raise PermissionError(f"Permission denied: {e}")
    except IOError as e:
        raise IOError(f"An I/O error occurred while saving the file: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {e}")

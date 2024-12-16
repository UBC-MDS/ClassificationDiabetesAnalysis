import os
import pickle

def save_model(model, file_path):
    """
    Saves a machine learning model or pipeline to a file using pickle.

    Parameters:
    -----------
    model : any
        The model or object to be saved.
    file_path : str
        Path to save the pickle file.

    Raises:
    -------
    IOError
        If there is an error saving the file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    try:
        with open(file_path, 'wb') as f:
            pickle.dump(model, f)
    except IOError as e:
        raise IOError(f"Error saving model to '{file_path}': {e}")

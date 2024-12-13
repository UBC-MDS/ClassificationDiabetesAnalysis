# read_zip.py
# author: Jenny Zhang
# date: 2024-12-12

import os
import zipfile
import requests

def read_zip(url, directory):
    """
    Read a zip file from the given URL and extract its contents to the specified directory.

    Parameters:
    ----------
    url : str
        The URL of the zip file to be read.
    directory : str
        The directory where the contents of the zip file will be extracted.

    Returns:
    -------
    None
    """
    request = requests.get(url)
    filename_from_url = os.path.basename(url)

    # check if URL exists, if not raise an error
    if request.status_code != 200:
        raise ValueError('The URL provided does not exist.')
    
    # check if the URL points to a zip file, if not raise an error  
    if request.headers['content-type'] != 'application/zip' or filename_from_url[-4:] != '.zip':
        raise ValueError('The URL provided does not point to a zip file.')
    
    # check if the directory exists, if not raise an error
    if not os.path.isdir(directory):
        raise ValueError('The directory provided does not exist.')

    # write the zip file to the directory
    path_to_zip_file = os.path.join(directory, filename_from_url)
    with open(path_to_zip_file, 'wb') as f:
        f.write(request.content)

    # get list of files/directories in the directory
    original_files = os.listdir(directory)
    original_timestamps = []
    for filename in original_files:
        filename = os.path.join(directory, filename)
        original_timestamp = os.path.getmtime(filename)
        original_timestamps.append(original_timestamp)

    # extract the zip file to the directory
    with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(directory)

    # check if any files were extracted, if not raise an error
    # get list of files/directories in the directory
    current_files = os.listdir(directory)
    current_timestamps = []
    for filename in current_files:
        filename = os.path.join(directory, filename)
        current_timestamp = os.path.getmtime(filename)
        current_timestamps.append(current_timestamp)
    if (len(current_files) == len(original_files)) & (original_timestamps == current_timestamps):
        raise ValueError('The ZIP file is empty.')

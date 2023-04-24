import json
import os
import logging
import dataclasses, json
import csv
import io

# def load_string(filepath: str, default=None):
#     if os.path.isfile(filepath) == False and os.access(filepath, os.R_OK) == False:
#          with io.open(os.path.join(filepath), 'r') as _:
#             logging.info(f"file_utils.py: No file at {filepath}")
#             return default
#     with open(filepath, 'r') as f:
#         return f.read()

def load_json(filepath: str, default=None):
    """
    Create or load a file

    Loads an exiting file if it exists, otherwise creates a new one.

    Parameters:
    filepath (str): Filepath to the file to be created or loaded.

    Returns:
    A file object.

    """
    # file = load_file(filepath, default)
    # return json.load(file)
    if os.path.isfile(filepath) == False and os.access(filepath, os.R_OK) == False:
         with io.open(os.path.join(filepath), 'w') as db_file:
            logging.info(f"file_utils.py: Creating new file at {filepath}")
            db_file.write(json.dumps(default))
    with open(filepath, 'r') as f:
        return json.load(f)

# def load_json_as_list(filepath: str, default=None) -> list[any]:
#     file = load_json(filepath, default)
#     return json.dumps(file)

def save_file(filepath, data):
    """
    Save a file

    Parameters:
    filepath (str): Filepath to the file to be saved.
    data (str): Data to be saved to the file.

    Returns:
    A file object.

    """
    if os.path.isfile(filepath) == False and os.access(filepath, os.R_OK) == False:
        with io.open(os.path.join(filepath), 'w') as db_file:
            logging.info(f"file_utils.py: Creating new file at {filepath}")
            db_file.write("")
    with open(filepath, 'w+') as f:
        f.write(data) 

def delete_file(filepath):
    os.remove(filepath)
"""
Data file management utilities
"""

import os


def is_development(path):
    """
    Return True if the path represents a development environment

    :param path: Path to examine
    :return: True if the path represents a development environment
    """
    parts = os.path.normpath(path.lower()).split(os.sep)
    for folder in ["development"]:
        if folder in parts:
            return True

    return False


def get_project_path():
    """
    Return the path to the root folder of the project

    :return: The path to the project root folder
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))


def get_data_path():
    """
    Return the path to the project's data folder

    :return: The path to the data folder
    """
    if not is_development(__file__) and "CHESS_ANALYSIS_DATA_FOLDER" in os.environ:
        data_folder = os.environ["CHESS_ANALYSIS_DATA_FOLDER"]
    else:
        data_folder = os.path.join(get_project_path(), "data")
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)

    return data_folder

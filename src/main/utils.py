import os
import pathlib
from configparser import ConfigParser, NoSectionError, NoOptionError


def get_api_key():
    config = ConfigParser()
    
    # Normalized file path (config.ini in the same folder as other modules)
    config_file_path = os.path.abspath(os.path.join(
        pathlib.Path(__file__).parent.resolve(), "config.ini"
    ))
    config.read(config_file_path)

    if not config.sections():  # check for config.ini in subfolder
        config_file_path = os.path.abspath(os.path.join(
            pathlib.Path(__file__).parent.resolve(), "config.ini"
        ))
    
    if not config.sections():  # check file not found error
        raise FileNotFoundError(f"No sections found in file at {config_file_path}. Is the file empty or missing?")
    
    return config["keys"]["api_key"], config["keys"]["api_secret"]
    

api_key, api_secret = get_api_key()

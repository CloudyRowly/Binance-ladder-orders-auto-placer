import os
import pathlib
from configparser import ConfigParser, NoSectionError, NoOptionError

class Accounts():
    def __init__(self):
        self.accounts = []
        self.config = ConfigParser()
        self.get_config()
        self.get_accounts()
    

    def get_config(self):
        # Normalized file path (config.ini in the same folder as other modules)
        config_file_path = os.path.abspath(os.path.join(
            pathlib.Path(__file__).parent.resolve(), "config.ini"
        ))

        self.config.read(config_file_path)
        print ()

        if not self.config.sections():  # check for config.ini in subfolder
            config_file_path = os.path.abspath(os.path.join(
                pathlib.Path(__file__).parent.resolve(), "config.ini"
            ))
            self.config.read(config_file_path)

        if not self.config.sections():  # check file not found error
            raise FileNotFoundError(f"No sections found in file at {config_file_path}. Is the file empty or missing?")


    def get_api_key(self, user):
        # get keys corresponding to user
        return self.config[user]["api_key"], self.config[user]["api_secret"]


    def get_accounts(self):
        self.accounts = self.config.sections()
        return self.accounts

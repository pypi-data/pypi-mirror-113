import os
from os.path import expanduser
from pathlib import Path

class Configuration():
    """
    A global configuration object that be loaded and used to read
    global settings.

    Settings resolution is:

    1. Look for GLOBAL variables
    2. Look in .<app>.config.yml in home directory
    3. Look in .local/<app>/config.yml
    """
    @staticmethod
    def getInstance():

        if Configuration.__instance == None:
            Configuration()
        return Configuration.__instance


    def __init__(self, app_name, config_vars=None):
        """
        Initializes the Configuration instance. This class is a singleton.
        """

        if hasattr(Configuration, "__instance") and Configuration.__instance != None:
            raise Exception("This class is a singleton But we created a new one")
        else:
            Configuration.__instance = self
            self.app_name = app_name
            if config_vars is None:
                self.config_vars = {}
            else:
                self.config_vars = config_vars

    def get_env(self, name):
        """
        Attempts to load a value from environment variables.
        returns None if it is not found.
        """
        try:
            value = os.environ[name]
            return value
        except KeyError as e:
            return None

    def __getattr__(self, item):
        if item in self.config_vars.keys():
            return self.get_config_var(item)

    def get_config_var(self,item):
        #First try to find it in the environment Vars

        value = self.get_env(item)
        if value is not None:
            return value
        msg = f"Could not find value for: {item}"
        raise ConfigSettingsNotFound(msg)

        #If we get here it means we don't have the value.
        #try looking for a config file from the home dir.

        #home = expanduser("~")
        #config_file = Path(home, self.app_name.lower())
        #if config_file.exists():

    #Great we have a configuration file!
    def load_config_vars_from_file(self):
        pass






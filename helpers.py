import os
import configparser

# Method to read config file settings
def read_config():
    config = configparser.ConfigParser()

    if os.environ.get("Environment") == "Development":
        config.read('configurations.Development.ini')
    else:
        config.read('configurations.ini')

    return config
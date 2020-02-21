import os

from configparser import ConfigParser

DEFAULT_CONFIG_PATH = "config.ini"


def get_project_config(config_path = None) -> dict:

    """
        Returns :py:class:`ConfigParser` object which is set to return configuration from file 'config_path'
        The file is searched upon directory config/, so all extra config files must be placed here.

        If :py:attr:`config_path` is not provided, current directory is used.

    :param config_path: a filename of .ini file in `config/` directory.
    :return: an object :py:class:`ConfigParser` with "key-value" interface.
    """

    if not config_path:
        config_path = DEFAULT_CONFIG_PATH

    config = ConfigParser()

    location = os.path.join(os.path.dirname(__file__),config_path)
    config.read(location)

    return config



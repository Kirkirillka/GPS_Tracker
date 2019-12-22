import os
from yaml import safe_load


def read_logging_config():
    """
        Read logging configuration from YAML
    :return:
    """

    location = os.path.join(os.path.dirname(__file__), "config.yml")

    with open(location) as file:
        return safe_load(file)
import os
from yaml import safe_load

import logging
import logging.config

MODULE_PARENT_LOGGER_NAME = 'gps_tracker'


def get_child_logger_by_name(*args):

    full_name_path = MODULE_PARENT_LOGGER_NAME + "." +".".join(list(args))

    return logging.getLogger(full_name_path)


def read_logging_config():
    """
        Read logging configuration from YAML
    :return:
    """

    location = os.path.join(os.path.dirname(__file__), "config.yml")

    with open(location) as file:
        return safe_load(file)


# create logger with 'spam_application'
logger = logging.getLogger(MODULE_PARENT_LOGGER_NAME)
logging.config.dictConfig(read_logging_config())
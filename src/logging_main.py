import os

import yaml

from logging import config, getLogger

def handler(logger_name, logger_level, logger_message):
    logging_config_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../config/logging_config.yml")
    )
    config.dictConfig(yaml.safe_load(open(logging_config_path).read()))
    logger = getLogger(logger_name)
    if logger_level == "INFO":
        logger.info(logger_message)
    elif logger_level == "WARNING":
        logger.warning(logger_message)
    elif logger_level == "ERROR":
        logger.error(logger_message)
    elif logger_level == "CRITICAL":
        logger.critical(logger_message)
    else:
        logger.debug(logger_message)

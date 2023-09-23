import datetime
import os
import sys

import yaml

from . import logging_main


def load_setting_file():
    """
    load yaml file and return dict.
    yaml_path: ./config/settings.yaml
    :return: dict: yaml content
    """
    logger_name = __name__
    yaml_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../config/settings.yaml")
    )
    yaml_file = ""
    try:
        with open(yaml_path) as yaml_files:
            yaml_file = yaml.safe_load(yaml_files)
    except FileNotFoundError as file_not_found:
        logging_main.handler(
            logger_name, "ERROR",
            f"{file_not_found}\nThe process will be aborted."
        )
        sys.exit(1)
    return yaml_file


def define_datetime_dict():
    """
    define date dict.
    format:
        datetime(current datetime): now
        date(year_month_day): "%Y%m%d"
        time(hour_minutes): "%H%M"
    :return: dict: datetime dict
    """
    datetime_dict = dict()
    now = datetime.datetime.now()
    date_year_month_day = now.strftime("%Y%m%d")
    time_hour_minutes = now.strftime("%H%M")
    datetime_dict["now"] = now
    datetime_dict["date_year_month_day"] = date_year_month_day
    datetime_dict["time_hour_minutes"] = time_hour_minutes
    return datetime_dict
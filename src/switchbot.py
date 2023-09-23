import json
import requests
import os
import sys

from dotenv import load_dotenv

from . import logging_main

from .utilities import load_setting_file
from .utilities import define_datetime_dict
from .mysql_operator import select_value

class SwitchBotOperator:
    def __init__(self):
        """
        initial Switchbot and MySQL info
        """
        load_dotenv()
        self.yaml_contents = load_setting_file()
        self.logger_name = __name__
        # define switchbot info
        try:
            self.switchbot_developer_token = \
                os.environ["SWITCHBOT_DEVELOPER_TOKEN"]
            self.switchbot_device_id = os.environ["SWITCHBOT_DEVICE_ID"]
            self.switchbot_info = self.yaml_contents["switchbot"]
            self.api_base_url = self.switchbot_info["api_base_url"]
            self.switchbot_api_url = \
                self.api_base_url + self.switchbot_device_id + "/commands"
            self.headers = {
                'Content-Type': 'application/json; charset: utf8',
                'Authorization': self.switchbot_developer_token
            }
        except KeyError as environ_error:
            logging_main.handler(
                self.logger_name, "ERROR",
                f"{environ_error}\nThe process will be aborted."
            )
            sys.exit(1)
        # get temperature and humidity
        ## MySQL info
        try:
            self.db_host = os.environ["MYSQL_HOST"]
            self.db_user = os.environ["MYSQL_USER"]
            self.db_password = os.environ["MYSQL_PASSWORD"]
            self.db_port = int(os.environ["MYSQL_PORT"])
            self.db_name = os.environ["MYSQL_DB_NAME"]
        except KeyError as environ_error:
            logging_main.handler(
                self.logger_name, "ERROR",
                f"{environ_error}\nThe process will be aborted."
            )
            sys.exit(1)
        ## MySQL table info
        try:
            self.table_name_settings = self.yaml_contents["TableName"]
            self.temperature_table = self.table_name_settings["temperature"]
            self.humidity_table = self.table_name_settings["humidity"]
        except KeyError as key_error:
            logging_main.handler(
                self.logger_name, "ERROR",
                f"{key_error}\nThe process will be aborted."
            )
            sys.exit(1)
        self.temperature, self.humidity = self._get_temperature_humidity()

        # define power off time
        self.home_control_info = self.yaml_contents["HomeControl"]
        self.power_off_time = self.home_control_info["power_off_hour_minutes"]
        self.now_time_hour_minutes = \
            define_datetime_dict()["time_hour_minutes"]

    def air_conditioning_controller(self):
        """
        control air conditioning
        :return: None
        """
        if self.now_time_hour_minutes == self.power_off_time:
            status_code = self._airconditioner_operation_poweroff()
            message = (f"air conditioning system Power OFF. "
                       f"status_code: {status_code}")
            logging_main.handler(
                self.logger_name, "INFO", message
            )

        else:
            # TODO: control air conditioning
            self._airconditioner_operation_poweron()

    def _airconditioner_operation_poweron(self):
        pass

    def _airconditioner_operation_poweroff(self):
        body = {
            "command": "setAll",
            "parameter": "27,3,3,off",
            "commandType": "command"
        }
        encoding_json = json.dumps(body)
        # print(encoding_json)
        poweroff_operation = requests.post(
            self.switchbot_api_url, data=encoding_json, headers=self.headers
        )
        return_status_code = poweroff_operation.status_code
        return return_status_code

    # get temperature and humidity value by MySQL
    def _get_temperature_humidity(self):
        temperature_value = select_value(
            self.db_host, self.db_user, self.db_password, self.db_port,
            self.db_name, table_name=self.temperature_table
        )
        humidity_value = select_value(
            self.db_host, self.db_user, self.db_password, self.db_port,
            self.db_name, table_name=self.humidity_table
        )
        message = (f"temperature: {temperature_value}°, "
                   f"humidity: {humidity_value}%")
        logging_main.handler(
            "status", "INFO",
            message
        )
        return temperature_value, humidity_value
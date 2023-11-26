import json
import requests
import os
import sys

from dotenv import load_dotenv

from . import logging_main

from .utilities import load_setting_file
from .utilities import define_datetime_dict
# from .mysql_operator import select_value
from . import mysql_operator

class SwitchBotOperator:
    def __init__(self):
        """
        initial Switchbot and MySQL info
        """
        load_dotenv()
        self.yaml_contents = load_setting_file()
        self.logger_name = __name__
        # define switchbot info and table name
        try:
            # switchbot info
            self.switchbot_developer_token = \
                os.environ["SWITCHBOT_DEVELOPER_TOKEN"]
            self.switchbot_device_id = os.environ["SWITCHBOT_DEVICE_ID"]
            self.switchbot_humidifier_ble_id = \
                os.environ["SWITCHBOT_HUMIDIFIER_BLE_ID"]
            self.switchbot_info = self.yaml_contents["switchbot"]
            self.api_base_url = self.switchbot_info["api_base_url"]
            self.switchbot_api_url = \
                self.api_base_url + self.switchbot_device_id + "/commands"
            self.switchbot_humidifier_url = \
                self.api_base_url + self.switchbot_humidifier_ble_id + \
                "/commands"
            self.headers = {
                'Content-Type': 'application/json; charset: utf8',
                'Authorization': self.switchbot_developer_token
            }
            # table name
            self.table_name = self.yaml_contents["TableName"]
        except KeyError as environ_error:
            logging_main.handler(
                self.logger_name, "ERROR",
                f"{environ_error}\nThe process will be aborted."
            )
            sys.exit(1)
        # get temperature and humidity
        mysql_instance = mysql_operator.DbOperation(self.table_name)
        self.temperature_value, self.humidity_value = \
            mysql_instance.get_mysql_record()

        # define power off time
        self.home_control_info = self.yaml_contents["HomeControl"]
        self.power_off_time = self.home_control_info["power_off_hour_minutes"]
        self.now_time_hour_minutes = \
            define_datetime_dict()["time_hour_minutes"]

    def controller(self):
        if self.now_time_hour_minutes == self.power_off_time:
            logger_message = ("airconditoning system and humidifier system "
                              "shutdown process start")
            message_severity = "INFO"
            self._logger_controller(logger_name=self.logger_name,
                                    severity=message_severity,
                                    message=logger_message)
            self._airconditioner_operation_poweroff()
            self._humidifier_operation_poweroff()
        else:
            if self.temperature_value is None and self.humidity_value is None:
                logger_message = (
                    "SQL Query result is None. ")
                message_severity = "ERROR"
                self._logger_controller(logger_name=self.logger_name,
                                        severity=message_severity,
                                        message=logger_message)
            else:
                pass

    def _logger_controller(self, logger_name, severity, message):
        logging_main.handler(
            logger_name, severity, message
        )

    def _airconditioner_operation_poweron(self):
        pass

    def _airconditioner_operation_poweroff(self):
        logger_name = "air conditioning"
        body = {
            "command": "setAll",
            "parameter": "27,3,3,off",
            "commandType": "command"
        }
        encoding_json = json.dumps(body)
        poweroff_operation = requests.post(
            self.switchbot_api_url, data=encoding_json, headers=self.headers
        )
        status_code = poweroff_operation.status_code
        if status_code == 200:
            status_message = (f"airconditioning system shutdown success. "
                              f"status code: {status_code}")
            message_severity = "INFO"
        else:
            status_message = (f"airconditioning system shutdown failed. "
                              f"status code: {status_code}")
            message_severity = "ERROR"
        self._logger_controller(logger_name=logger_name,
                                severity=message_severity,
                                message=status_message)

    def _humidifier_operation_poweron(self):
        pass

    def _humidifier_operation_poweroff(self):
        logger_name = "humidifier"
        body = {
            "command": "turnOff",
            "parameter": "default",
            "commandType": "command"
        }
        encoding_json = json.dumps(body)
        poweroff_operation = requests.post(
            self.switchbot_humidifier_url, data=encoding_json,
            headers=self.headers
        )
        status_code = poweroff_operation.status_code
        if status_code == 200:
            status_message = (f"humidifier system shutdown success. "
                              f"status code: {status_code}")
            message_severity = "INFO"
        else:
            status_message = (f"humidifier system shutdown failed. "
                              f"status code: {status_code}")
            message_severity = "ERROR"
        self._logger_controller(logger_name=logger_name,
                                severity=message_severity,
                                message=status_message)

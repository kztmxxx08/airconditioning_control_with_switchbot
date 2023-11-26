import os
import sys

import MySQLdb

from dotenv import load_dotenv

from . import logging_main


class DbOperation:
    def __init__(self, table_name):
        """
        initial Switchbot and MySQL info
        """
        load_dotenv()
        self.logger_name = __name__
        # Define MySQL info
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
        self.table_name = table_name

    def get_mysql_record(self):
        temperature_value, humidity_value = None, None
        try:
            conn = MySQLdb.connect(
                host=self.db_host, user=self.db_user,
                passwd=self.db_password, port=self.db_port, db=self.db_name
            )
        except MySQLdb.OperationalError as db_conn_error:
            logging_main.handler(
                self.logger_name, "ERROR",
                f"{db_conn_error}\nThe process will be aborted."
            )
            sys.exit(1)
        cur = conn.cursor()
        sql = (f"select temperature_value, humidity_value from "
               f"{self.table_name} ORDER BY data_time DESC LIMIT 1")
        try:
            cur.execute(sql)
        except MySQLdb.ProgrammingError as sql_execute_error:
            logging_main.handler(
                self.logger_name, "ERROR",
                f"{sql_execute_error}\nThe process will be aborted."
            )
            sys.exit(1)
        sql_result = cur.fetchone()
        if sql_result:
            temperature_value, humidity_value = sql_result
            logging_main.handler(
                self.logger_name, "INFO",
                f"Query is success. "
                f"temperature: {temperature_value},humidity: {humidity_value} "
            )
        else:
            logging_main.handler(
                self.logger_name, "ERROR",
                f"sql query result is empty. "
            )
        cur.close()
        conn.close()
        return temperature_value, humidity_value

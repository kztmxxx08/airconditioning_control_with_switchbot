import os
import unittest

from dotenv import load_dotenv

from src import mysql_operator


class MySQLOperator(unittest.TestCase):
    def test_select_value(self):
        load_dotenv()
        db_host = os.environ["MYSQL_HOST"]
        db_user = os.environ["MYSQL_USER"]
        db_password = os.environ["MYSQL_PASSWORD"]
        db_port = int(os.environ["MYSQL_PORT"])
        db_name = os.environ["MYSQL_DB_NAME"]
        table_name = "homemanagement_temperature"
        db_instance = mysql_operator.select_value(
            db_host, db_user, db_password, db_port, db_name, table_name
        )
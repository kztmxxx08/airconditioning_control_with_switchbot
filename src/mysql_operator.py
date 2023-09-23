import sys

import MySQLdb

from . import logging_main

def select_value(db_host, db_user, db_password, db_port, db_name, table_name):
    logger_name = __name__
    try:
        conn = MySQLdb.connect(
            host=db_host, user=db_user, passwd=db_password, port=db_port,
            db=db_name
        )
    except MySQLdb.OperationalError as db_conn_error:
        logging_main.handler(
            logger_name, "ERROR",
            f"{db_conn_error}\nThe process will be aborted."
        )
        sys.exit(1)
    cur = conn.cursor()
    sql = f"select value from {table_name}"
    try:
        cur.execute(sql)
    except MySQLdb.ProgrammingError as sql_execute_error:
        logging_main.handler(
            logger_name, "ERROR",
            f"{sql_execute_error}\nThe process will be aborted."
        )
        sys.exit(1)
    response = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return response

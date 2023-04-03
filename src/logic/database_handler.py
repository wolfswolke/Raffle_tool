"""
"""

# --------------------------------------- #
#               imports                   #
# --------------------------------------- #

from zk_tools.logging_handle import logger

import sqlite3
from sqlite3 import Error
import os
from datetime import datetime

# --------------------------------------- #
#              definitions                #
# --------------------------------------- #
MODULE_LOGGER_HEAD = "database_handler -> "

# --------------------------------------- #
#              global vars                #
# --------------------------------------- #
db_file = r"database\\sqlite.db"

# --------------------------------------- #
#              functions                  #
# --------------------------------------- #


def date_handle():
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    return current_date


def error_handler(error_val):
    logger.error(MODULE_LOGGER_HEAD + "An Error occurred. Please read the following message for more info.")
    error_statement = str(error_val)
    logger.error(MODULE_LOGGER_HEAD + error_statement)


def setup_database():
    logger.info(MODULE_LOGGER_HEAD + "Reset of Database started")
    if os.path.isfile(db_file):
        logger.debug(MODULE_LOGGER_HEAD + "Removing Old db...")
        os.remove(db_file)

    conn = None
    try:
        conn = sqlite3.connect(db_file)
        logger.debug(MODULE_LOGGER_HEAD + sqlite3.version)
    except Error as e:
        error_handler(e)
    finally:
        logger.info(MODULE_LOGGER_HEAD + "DB Writen.")
        if conn:
            sql_creation_template = """CREATE TABLE personal (
   ID INTEGER PRIMARY KEY,
   date TEXT DEFAULT CURRENT_TIMESTAMP,
   personal_nummer integer NOT NULL,
   value integer NOT NULL,
   last_change DATE NOT NULL
);"""
            try:
                c = conn.cursor()
                c.execute(sql_creation_template)
            except Error as e:
                error_handler(e)
            conn.close()


def read_db():
    logger.debug(MODULE_LOGGER_HEAD + "Reading Database")
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("SELECT * FROM personal")
    query = cur.fetchall()
    con.close()
    logger.debug(MODULE_LOGGER_HEAD + "Finished reading")
    return query


def read_personal_nummer_db():
    logger.debug(MODULE_LOGGER_HEAD + "Reading Database")
    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("SELECT personal_nummer FROM personal")
    query = cur.fetchall()
    con.close()
    logger.debug(MODULE_LOGGER_HEAD + "Finished reading")
    return query


def write_db(personal_nummer, new_value):
    logger.info(MODULE_LOGGER_HEAD + "Writing these Values to DB: {} {}".format(personal_nummer, new_value))
    current_date = date_handle()
    query = """INSERT INTO personal(personal_nummer, value, last_change) VALUES ({}, {}, "{}");""".format(personal_nummer, new_value, current_date)
    sq_execute_handler(query)
    logger.debug(MODULE_LOGGER_HEAD + "Finished writing")


def alter_db(personal_nummer, new_value):

    con = sqlite3.connect(db_file)
    cur = con.cursor()
    cur.execute("""Select value FROM personal WHERE personal_nummer = {}""".format(personal_nummer))
    read_query = cur.fetchall()
    con.close()

    for items in read_query:
        for item in items:
            return_value = item - new_value
    logger.debug(MODULE_LOGGER_HEAD + "Changing User {} to this Value {}.".format(personal_nummer, return_value))
    current_date = date_handle()
    query = """Update personal SET value = {} WHERE personal_nummer = {}""".format(return_value, personal_nummer, current_date)
    sq_execute_handler(query)


def alter_db_positive(new_value):
    all_users = read_db()
    for item in all_users:
        value = item[3] + new_value
        logger.debug(MODULE_LOGGER_HEAD + "Changing User {} to this Value {}.".format(item[2], value))
        current_date = date_handle()
        query = """Update personal SET value = {} WHERE personal_nummer = {}""".format(value, item[2], current_date)
        sq_execute_handler(query)


def remove_db(personal_nummer):
    logger.info(MODULE_LOGGER_HEAD + "User {} not found. Removing from DB".format(personal_nummer))
    query = """DELETE from personal where personal_nummer = {}""".format(personal_nummer)
    sq_execute_handler(query)


def sq_execute_handler(query):
    try:
        conn = sqlite3.connect(db_file)
        if conn:
            logger.debug(MODULE_LOGGER_HEAD + "Conn stable. Writing now...")
            try:
                c = conn.cursor()
                c.execute(query)
                conn.commit()
            except Error as e:
                error_handler(e)
            conn.close()

    except Exception as e:
        error_handler(e)


# --------------------------------------- #
#               classes                   #
# --------------------------------------- #



"""
"""
# --------------------------------------- #
#               imports                   #
# --------------------------------------- #
import csv

from zk_tools.logging_handle import logger
from zk_tools.config_handle import config

from logic.database_handler import setup_database
from logic.database_handler import read_db
from logic.database_handler import alter_db_positive
from logic.database_handler import write_db
from logic.database_handler import read_personal_nummer_db
from logic.database_handler import remove_db
from logic.raffle import start_raffle

# --------------------------------------- #
#              definitions                #
# --------------------------------------- #
MODULE_LOGGER_HEAD = "start_app -> "
APP_VERSION = "v01-00-00"


# --------------------------------------- #
#              global vars                #
# --------------------------------------- #

winning_price = 0
entry_value = 0
prices = 0


# --------------------------------------- #
#              functions                  #
# --------------------------------------- #
def setup_logging(level):
    logger.set_logging_level(level)
    logger.set_cmd_line_logging_output()


def setup_global_vars():
    logger.debug(MODULE_LOGGER_HEAD + "Settings Global Vars")
    global winning_price
    winning_price = config.get_element("prices", "winning_price")
    global entry_value
    entry_value = config.get_element("defaults", "entry_value")
    global prices
    prices = config.get_element("prices", "things_to_win")
    logger.debug(MODULE_LOGGER_HEAD + "Values Set. Leaving setup_global_vars")

# --------------------------------------- #
#               classes                   #
# --------------------------------------- #


# --------------------------------------- #
#                main                     #
# --------------------------------------- #
if __name__ == "__main__":
    try:
        config.load_config("../config/config_raffle.yml")
        config.set_element("general", "version", APP_VERSION)

        setup_logging(config.get_element("general", "debug_level"))

        logger.info("-----------------------------------------------------------")
        logger.info("            Started Raffle Tool {}".format(APP_VERSION))
        logger.info("-----------------------------------------------------------")

        setup_global_vars()

        if config.get_element("overwrites", "reset"):
            logger.info(MODULE_LOGGER_HEAD + "Reseting Database...")
            setup_database()
            logger.info(MODULE_LOGGER_HEAD + "Database Reset")

        if config.get_element("overwrites", "match_users_to_csv"):
            with open('file.csv', 'r') as f:
                reader = csv.reader(f)
                user_list = list(reader)

                reset_list_personal_nummern = []
                reset_list_csv = []
                alle_personal_nummern = read_personal_nummer_db()
                for nummern in alle_personal_nummern:
                    for items in nummern:
                        reset_list_personal_nummern.append(items)

                for value in user_list:
                    for item in value:
                        item = int(item)
                        reset_list_csv.append(item)
                        if item in reset_list_personal_nummern:
                            logger.debug(MODULE_LOGGER_HEAD + "The Person {} is already in DB. Skipping.".format(item))
                        else:
                            logger.debug(MODULE_LOGGER_HEAD + "Writing {} to DB.".format(item))
                            write_db(item, entry_value)

                for nummern in alle_personal_nummern:
                    for items in nummern:
                        if items not in reset_list_csv:
                            remove_db(items)

        if config.get_element("overwrites", "start_raffle"):
            logger.info("Verlosung wird gestartet")
            db_read = read_db()
            current_contestants = list()
            for items in read_db():
                for _ in range(items[3]):
                    current_contestants.append(items[2])
            start_raffle(db_read, prices, current_contestants, winning_price)
            alter_db_positive(winning_price)

    except KeyboardInterrupt:
        logger.info("-----------------------------------------------------------")
        logger.info("            Raffle Tool Stopped")
        logger.info("-----------------------------------------------------------")

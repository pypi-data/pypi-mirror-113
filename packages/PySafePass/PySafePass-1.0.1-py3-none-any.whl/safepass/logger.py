import logging 
import sys
from safepass.paths import log_file


logging.basicConfig(filename=log_file, encoding='utf-8', level=logging.DEBUG)


def info(log:str):
    logging.info(log)


def warning(log:str):
    logging.warning(log)


def error(log:str):
    logging.error(log)


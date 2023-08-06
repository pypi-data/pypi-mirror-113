import logging 
import sys
from safepass.paths import log_file


logging.basicConfig(handlers=[logging.FileHandler(filename=log_file, 
                                                 encoding='utf-8',
                                                 mode='a+')],
                    format="%(asctime)s %(name)s:%(levelname)s:%(message)s", 
                    datefmt="%F %A %T", 
                    level=logging.DEBUG)


def info(log:str):
    logging.info(log)


def warning(log:str):
    logging.warning(log)


def error(log:str):
    logging.error(log)


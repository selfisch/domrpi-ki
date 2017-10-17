import logging
from os import mkdir, path

def setup_custom_logger(name):

    if not path.exists('log'):
        mkdir('log')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')

    handler = logging.FileHandler('log/aiwa.log')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

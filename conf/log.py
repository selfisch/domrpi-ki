import logging
from os import mkdir, path

def setup_custom_logger(name):

    if not os.path.exists('log'):
        os.mkdir('log')

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d')

    handler = logging.FileHandler('log/aiwa.log')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger

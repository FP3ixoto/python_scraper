from logtail import LogtailHandler
import logging
import helpers

config = helpers.read_config()

logtail_handler = LogtailHandler(source_token=config['LogtailHandler']['token'])

def create_default_logger(name):
    logger = logging.getLogger(name)
    logger.handlers = []
    logger.setLevel(logging.INFO)
    logger.addHandler(logtail_handler)
    return logger
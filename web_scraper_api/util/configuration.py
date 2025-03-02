import logging
import os


def get_key(key: str):
    try:
        return os.environ[key]
    except KeyError as keyError:
        raise Exception(f'No ENV Variable with name {keyError} found')


class Configuration:
    def __init__(self):
        self.webdriver_remote_host = get_key('WEBDRIVER_REMOTE_HOST')
        self.host = get_key('HOST')
        self.port = int(get_key('PORT'))
        self.api_key = get_key('X-API-KEY')
        self.log_level = logging.getLevelNamesMapping().get(get_key('LOG_LEVEL'))
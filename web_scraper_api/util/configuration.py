import os


def get_key(key: str):
    try:
        return os.environ[key]
    except KeyError as keyError:
        raise Exception(f'No ENV Variable with name {keyError} found')


class Configuration:
    def __init__(self):
        self.host = get_key('HOST')
        self.port = int(get_key('PORT'))
        self.driver_path = get_key('DRIVER_PATH')
        self.api_key = get_key('X-API-KEY')
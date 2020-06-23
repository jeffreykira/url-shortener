
CONFIG = None


class Config:

    SERVER_HOST = 'localhost'
    SERVER_PORT = 5604

    REDIS_HOST = SERVER_HOST
    REDIS_PORT = 6379
    REDIS_URL = 'redis://{}:{}/0'.format(REDIS_HOST, REDIS_PORT)

    URL_PREFIX = 'http://shorturl.at/'


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
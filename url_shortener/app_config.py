
CONFIG = None


class Config:

    SERVER_HOST = 'localhost'
    SERVER_PORT = 5604


class ProdConfig(Config):
    DEBUG = False


class DevConfig(Config):
    DEBUG = True
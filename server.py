import logging
import logging.config
import os
import time
import traceback
import subprocess
from url_shortener import app_config
from url_shortener import logging_config
from url_shortener.api import api_proxy
from flask import Flask, Blueprint, request, g
from shutil import which

logging.config.dictConfig(logging_config.LOGGING)
log = logging.getLogger(__name__)

if os.environ.get('SHORTEN_ENV') == 'PROD':
    app_config.CONFIG = app_config.ProdConfig
else:
    app_config.CONFIG = app_config.DevConfig

if which('docker') is None:
    raise Exception('docker is not installed.')
if which('docker-compose') is None:
    raise Exception('docker-compose is not installed.')
# TODO run redis docker

flask_app = Flask(__name__)
flask_app.config.from_object(app_config.CONFIG)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api_proxy.init(blueprint)
flask_app.register_blueprint(blueprint)


if __name__ == '__main__':
    try:
        flask_app.run(host=app_config.CONFIG.SERVER_HOST, port=app_config.CONFIG.SERVER_PORT)
    except Exception:
        traceback.print_exc()

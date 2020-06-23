import logging
import logging.config
import os
import time
import traceback
import subprocess
from url_shortener import app_config
from url_shortener import logging_config
from url_shortener.api import api_proxy
from url_shortener import database as DB
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
subprocess.run('docker-compose -f url_shortener/docker-compose.yml up -d database', shell=True)

flask_app = Flask(__name__)
flask_app.config.from_object(app_config.CONFIG)

DB.init(flask_app)

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api_proxy.init(blueprint)
flask_app.register_blueprint(blueprint)


@flask_app.before_request
def before_request():
    log.info('request: {}'.format(' '.join([request.remote_addr, request.method, request.url])))
    if flask_app.config['DEBUG']:
        g.request_start_time = time.time()
        g.request_time = lambda: '%.5fs' % (time.time() - g.request_start_time)
        log.debug('request header: {}'.format(', '.join(': '.join(x) for x in request.headers)))
        log.debug('request data: {}'.format(request.get_data(as_text=True)))


@flask_app.after_request
def after_request(response):
    if flask_app.config['DEBUG']:
        response.headers.add('x-time-elapsed', g.request_time())

    return response


if __name__ == '__main__':
    try:
        flask_app.run(host=app_config.CONFIG.SERVER_HOST, port=app_config.CONFIG.SERVER_PORT)
    except Exception:
        traceback.print_exc()

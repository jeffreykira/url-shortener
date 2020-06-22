import flask_restplus
import importlib
import logging
import os
from url_shortener import app_config
from url_shortener import utils
from url_shortener.exception import *

log = logging.getLogger(__name__)
api = flask_restplus.Api(version='1.0.0', title='URL Shortener API', description='API Document')


@api.errorhandler
def default_error_handler(e):
    log.exception(e)
    message = 'An unhandled exception occurred.'
    return {'message': message}, 500


def _error_handler(e, code):
    message = '{}: [{}]'.format(e.__class__.__name__, e)
    log.exception(e)
    return {'message': message}, code


@api.errorhandler(DataValidationError)
def data_validation_error_handler(e):
    return _error_handler(e, 403)


@api.errorhandler(ResourceNotFound)
def resource_not_found_error_handler(e):
    return _error_handler(e, 404)


@utils.log_scope(log)
def init(app):
    if not app_config.CONFIG.DEBUG:
        api._doc = False

    api.init_app(app)

    import url_shortener
    for model_name in [os.path.splitext(f)[0] for f in os.listdir(list(url_shortener.api.__path__)[0])]:
        if model_name.endswith('_endpoint'):
            m = importlib.import_module('url_shortener.api.' + model_name)
            log.debug('endpoint: {} added.'.format(m.__name__))

    log.info('inited.')
import logging
from flask_redis import FlaskRedis
from url_shortener import utils

log = logging.getLogger(__name__)
redis_client = FlaskRedis()


@utils.log_scope(log)
def set_item(name, value):
    redis_client.set(name, value)


@utils.log_scope(log)
def get_item(name):
    return redis_client.get(name)


@utils.log_scope(log)
def init(app):
    redis_client.init_app(app)

    log.info('inited.')
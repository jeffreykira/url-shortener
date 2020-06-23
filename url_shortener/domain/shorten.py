import logging
import hashlib
import requests
from url_shortener import utils
from url_shortener import app_config
from url_shortener import database as DB
from url_shortener.exception import *

log = logging.getLogger(__name__)


def _shorten_code(url):
    if not isinstance(url, str):
        raise DataValidationError()

    return hashlib.md5(url.encode('utf-8')).hexdigest()[-5:]


@utils.log_scope(log)
def create(url):
    if not url.lower().startswith(('http://', 'https://')):
        raise DataValidationError('url schema error')

    try:
        req = requests.get(url)
    except Exception:
        raise ResourceNotFound('URL does not exist')

    if req.status_code != 200:
        raise ResourceNotFound('URL does not exist')

    short_code = _shorten_code(url)
    short_url = app_config.CONFIG.URL_PREFIX + short_code

    DB.set_item(short_code, url)

    return short_url
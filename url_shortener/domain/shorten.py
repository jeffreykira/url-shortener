import logging
import hashlib
from url_shortener import utils
from url_shortener import app_config
from url_shortener.exception import *

log = logging.getLogger(__name__)


def _shorten_code(url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()[-5:]


@utils.log_scope(log)
def create(url):
    if not isinstance(url, str):
        raise DataValidationError()

    short_code = _shorten_code(url)
    short_url = app_config.CONFIG.URL_PREFIX + short_code

    return short_url
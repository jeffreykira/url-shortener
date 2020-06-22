from flask_restplus import fields
from url_shortener.api.api_proxy import api


url = api.model('url', {
    'url': fields.String(required=True, descirption='url', example='https://www.google.com/')
})

shorten_url = api.model('shorten_url', {
    'short_url': fields.String(required=True, descirption='short url', example='http://shorturl.at/zxcvb')
})

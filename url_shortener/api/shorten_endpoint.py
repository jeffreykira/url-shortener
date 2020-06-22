import logging
from flask import request
from flask_restplus import Resource
from url_shortener.api import shorten_endpoint_model as model
from url_shortener.api.api_proxy import api
from url_shortener.domain import shorten as ShortenDomain

log = logging.getLogger(__name__)
namespace = api.namespace('shorten', description='Shortener service.')


@namespace.route('')
class Shorten(Resource):

    @api.expect(model.url, validate=True)
    @api.marshal_with(model.shorten_url, code=201)
    @api.response(201, 'Success')
    @api.response(403, 'DataValidationError')
    def post(self):
        '''
        Shortener a URL.
        '''
        data = request.json
        short_url = ShortenDomain.create(data.get('url'))
        return {'short_url': short_url}, 201
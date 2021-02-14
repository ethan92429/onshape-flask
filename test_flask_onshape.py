import logging
import unittest

import requests
from mock import patch, Mock

from flask import Flask, request, redirect
from flask_onshape import Onshape

logger = logging.getLogger(__name__)


class OnshapeTestCase(unittest.TestCase):

    @patch.object(requests.Session, 'post')
    @patch.object(Onshape, 'BASE_AUTH_URL')
    def test_authorization(self, auth_url, post):
        def assert_params(*args, **kwargs):
            data = kwargs.pop('data')
            assert data['client_id'] == '123'
            assert data['client_secret'] == 'SEKRET'
            assert data['code'] == 'KODE'
            response = Mock()
            response.content = '{"access_token":"asdf","token_type":"bearer"}'
            return response
        post.side_effect = assert_params
        auth_url.__get__ = Mock(return_value='http://localhost/oauth/')

        app = Flask(__name__)

        app.config['ONSHAPE_CLIENT_ID'] = '123'
        app.config['ONSHAPE_CLIENT_SECRET'] = 'SEKRET'

        onshape = Onshape(app)

        @app.route('/login')
        def login():
            return onshape.authorize(redirect_uri="http://localhost/callback")

        @app.route('/callback')
        @onshape.authorized_handler
        def authorized(token):
            access_token.append(token)
            return ''

        # Mimics Onshape authorization URL
        # https://onshape-public.onshape.io/docs/oauth/
        @app.route('/oauth/authorize')
        def handle_auth():
            logger.info("in /oauth/authorize")
            called_auth.append(1)
            assert request.args['client_id'] == '123'
            logger.debug("client_id OK")
            assert request.args['redirect_uri'] == 'http://localhost/callback'
            logger.debug("redirect_uri OK")
            return redirect(request.args['redirect_uri'] + '?code=KODE')

        access_token = []
        called_auth = []

        client = app.test_client()
        client.get('/login', follow_redirects=True)

        assert called_auth
        assert access_token == ['asdf'], access_token


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()

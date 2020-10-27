"""Main entry point for Flask WSGI app."""
import flask
import flask_cors

from authlib.integrations.base_client import errors
from authlib.integrations import flask_client
from authlib.oauth2.rfc6749 import wrappers

from models import oauth2_token

import logging
import os
import requests

flask_app = flask.Flask(__name__)
# Required for both authlib and flask_login- both uses sessions internally.
flask_app.secret_key = b'\xad\x82\\\x10\x95\x8b\xe5\xca\xf3,?\x02I9\xee"'
# Setup flask_cors to avoid CORS errors during development.
# Errors are probably caused by microservice (multi-docker container) setup.
flask_cors.CORS(flask_app, origins=("localhost"))

logging.basicConfig(level=logging.DEBUG)

_SPOTIFY_API_ENDPOINT = 'https://api.spotify.com/v1/'

def _fetch_token(name):
  current_token = flask.session.get('current_token')
  return wrappers.OAuth2Token.from_dict(current_token)

_oauth = flask_client.OAuth(flask_app, fetch_token=_fetch_token)

# TODO (deojonathan@): Transfer this to a separate configuration file.
_oauth.register(
  name='spotify',
  client_id=os.environ.get('SPOTIFY_CLIENT_ID', ''),
  client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET', ''),
  authorize_url='https://accounts.spotify.com/authorize',
  access_token_url='https://accounts.spotify.com/api/token',
  api_base_url=_SPOTIFY_API_ENDPOINT,
  client_kwargs={
    'scope': 'user-read-private user-read-email',
  },
)

def _get_current_user():
  try:
    api = 'me'
    resp = _oauth.spotify.get(api)
  except errors.MissingTokenError:
    logging.error('Exception caught on _get_current_user()')
    return None
  return resp.json()

@flask_app.route('/login')
def login():
  redirect_uri = flask.url_for('authorize', _external=True)
  return _oauth.spotify.authorize_redirect(redirect_uri)

@flask_app.route('/authorize')
def authorize():
  current_token = _oauth.spotify.authorize_access_token()
  resp = _oauth.spotify.get('me')
  user_info = resp.json()

  # TODO(deojonathan@) Save this to DB and don't save to session.
  current_token = oauth2_token.OAuth2Token(
    username=user_info.get('display_name'),
    email=user_info.get('email'),
    access_token=current_token.get('access_token'),
    refresh_token=current_token.get('refresh_token'),
    token_type=current_token.get('token_type'),
    expires_at=current_token.get('expires_at')
  )
  flask.session['current_token'] = dict(current_token)
  return flask.jsonify(success=True)

@flask_app.route('/user', methods=['POST', 'GET'])
def get_current_user():
  current_user = _get_current_user()
  if current_user:
    return flask.jsonify(current_user)
  return flask.redirect('/login')

@flask_app.route('/token', methods=['POST'])
def get_current_token():
  if not _get_current_user():
    return flask.redirect('/login')
  return flask.jsonify(flask.session.get('current_token'))

@flask_app.route('/logout')
def logout():
  flask.session.clear()
  return flask.redirect(flask.url_for('login'))

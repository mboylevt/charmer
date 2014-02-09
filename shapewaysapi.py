# -*- coding: utf-8 -*-

from flask import redirect, request, Blueprint
from shapeways.client import Client

shapeways_api = Blueprint('shapeways_api', __name__)

# Shapeways API client and constants
client = Client(
    consumer_key='3436330b02d3c528e710723463c9c06c2524dcb7',
    consumer_secret='92af8366018489e8498fa87a34d442ab8de6e374',
    callback_url="http://localhost:5051/api/callback"
)
OAUTH_TOKEN = "oauth_token"
OAUTH_VERIFIER = "oauth_verifier"

# Shapeways API interactions

@shapeways_api.route('/api/register')
def api_register():
    """
    Register this application with the Shapeways API via oauth1.

    This is required on application startup
    """

    url = client.connect()
    return redirect(url, code=302)

@shapeways_api.route('/api/callback', methods=['GET'])
def api_callback():
    """
    Callback URL for Shapeways API registration

    The callback URL parameters will contain oauth_token and oauth_verifier
    """
    oauth_token = request.args.get(OAUTH_TOKEN)
    oauth_verifier = request.args.get(OAUTH_VERIFIER)
    client.verify(oauth_token, oauth_verifier)
    info = client.get_api_info()
    assert info['result'] == 'success', "API authentication failed"
    return redirect('http://localhost:5051/', 302)

@shapeways_api.route('/upload')
def api_upload():
    pass
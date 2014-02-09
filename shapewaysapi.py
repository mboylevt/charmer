# -*- coding: utf-8 -*-
import base64
import json

from flask import redirect, request, Blueprint, render_template
from urllib2 import urlopen
import requests
from shapeways.client import Client
from uuid import uuid4

shapeways_api = Blueprint('shapeways_api', __name__, template_folder='templates')

# Shapeways API client and constants
client = Client(
    consumer_key='3436330b02d3c528e710723463c9c06c2524dcb7',
    consumer_secret='92af8366018489e8498fa87a34d442ab8de6e374',
    oauth_token='887ba999bc041e92e74902dd9586926097c62fc5',
    oauth_secret='8ea37b2ad5e7920511af4b38805be36a9b482516',
    callback_url="http://localhost:5051/api/callback"
)

OAUTH_TOKEN = "oauth_token"
OAUTH_VERIFIER = "oauth_verifier"
MODEL_FILE_NAME = "modelFileName"
MODEL_FILE_PATH = "modelFilePath"

# Shapeways API interactions

@shapeways_api.route('/api/register')
def api_register():
    """
    Register this application with the Shapeways API via oauth1.

    This is required on application startup
    """

    url = client.connect()
    return redirect(url, code=302)

@shapeways_api.route('/api/test', methods=['GET'])
def api_test():
    client.connect()
    info = client.get_api_info()
    assert info['result'] == 'success', "API authentication failed"
    return redirect('http://localhost:5051/', 302)


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

@shapeways_api.route('/upload', methods=['POST'])
def api_upload():
    client.connect()
    model_file = requests.get(request.form[MODEL_FILE_PATH], timeout=30)
    file_data = base64.b64encode(model_file.content)
    model_name = request.form['title']
    params = {
        "fileName": model_name + '.x3db',
        "file": file_data,
        "hasRightsToModel": True,
        "acceptTermsAndConditions": True
    }
    response = client.add_model(params=params)
    return_params = {
        "modelId": response['modelId'],
        "title": model_name
    }
    return json.dumps(return_params)
from flask import Flask, Blueprint, Response, request, redirect, session, render_template, url_for
from flask_session import Session

import adal
import uuid
import requests
from . import config

main = Blueprint('main', __name__)

PORT = 5000  # Flask default port
AUTHORITY_URL = config.AUTHORITY_HOST_URL + '/' + config.TENANT
REDIRECT_URI = f'http://localhost:{PORT}/getAToken'
TEMPLATE_AUTHZ_URL = ('https://login.microsoftonline.com/{}/oauth2/authorize?' +
                      'response_type=code&client_id={}&redirect_uri={}&' +
                      'state={}&resource={}')

                      
@main.route('/', methods=["GET", "POST"])
def start():
    login_url = f'http://localhost:{PORT}/login'
    resp = Response(status=307)
    resp.headers['location'] = login_url
    return resp

@main.route('/login')
def login():
    auth_state = str(uuid.uuid4())
    session['state'] = auth_state
    authorization_url = TEMPLATE_AUTHZ_URL.format(
        config.TENANT,
        config.CLIENT_ID,
        REDIRECT_URI,
        auth_state,
        config.RESOURCE)
    resp = Response(status=307)
    resp.headers['location'] = authorization_url
    return resp

@main.route('/getAToken')
def main_logic():
    code = request.args['code']
    state = request.args['state']
    if state != session['state']:
        raise ValueError("State does not match")
    auth_context = adal.AuthenticationContext(AUTHORITY_URL)
    token_response = auth_context.acquire_token_with_authorization_code(
        code, 
        REDIRECT_URI, 
        config.RESOURCE,
        config.CLIENT_ID, 
        config.CLIENT_SECRET)
    session['access_token'] = token_response['accessToken']

    return redirect('/index')

@main.route('/index')
def index():
    if 'access_token' not in session:
        return redirect('login')
    return render_template('index.html')










# # @app.errorhandler(404)
# # def page_not_found():
# #     return render_template('404.html'), 404

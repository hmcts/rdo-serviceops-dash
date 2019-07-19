from flask import Flask, Blueprint, render_template

import os
import adal
import requests
import json

from azure.common.credentials import ServicePrincipalCredentials

from . import config

az = Blueprint('az', __name__)

@az.route('/azure_services')
def azure_services():

    tenant_id = '531ff96d-0ae9-462a-8d2d-bec7c0b42082'
    application_id = 'f2279271-d0a0-45ed-ac1c-5aff1388ff01'
    application_secret = '.RS[03PGSl]*1A1L[gTs4+DTuLrkf3*n'

    credentials = ServicePrincipalCredentials(
        client_id=application_id,
        secret=application_secret,
        tenant=tenant_id
    )

    authentication_endpoint = 'https://login.microsoftonline.com/'
    resource = 'https://management.core.windows.net/'

    # get an Azure access token using the adal library
    context = adal.AuthenticationContext(authentication_endpoint + tenant_id)
    token_response = context.acquire_token_with_client_credentials(
        resource, application_id, application_secret)

    access_token = token_response.get('accessToken')

    grafana_header = {"Authorization: Bearer eyJrIjoiSWJybHNxZmh5MDdENWdXbWZjc05UZEowandMVDZacGIiLCJuIjoiZmxhc2siLCJpZCI6MX0="}
    subscriptions = 'https://management.azure.com/subscriptions/?api-version=2015-01-01'
    headers = {"Authorization": 'Bearer ' + access_token}

    json_output_subscriptions = requests.get(subscriptions, headers=headers).json()
    data = json_output_subscriptions["value"]

    headers = {"Authorization": 'Bearer ' + access_token, "Content-Type": 'application/json'}

    return render_template('az_services/index.html', data=data, token=grafana_header)


@az.route('/azure_services/apps')
def azure_apps():
    return render_template('az_services/app_services.html')

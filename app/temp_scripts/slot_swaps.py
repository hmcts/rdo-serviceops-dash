from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.web import WebSiteManagementClient
import os, datetime

import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np


tenant_id = os.environ.get('TENANT')
application_id = os.environ.get('CLIENT_ID_JENKINS')   
application_secret = os.environ.get('CLIENT_SECRET_JENKINS') 
subscription_id = os.environ.get('SUBSCRIPTION_ID')

credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id,
)

web_client = WebSiteManagementClient(credentials, subscription_id)

web_apps = web_client.web_apps.list()

for app in web_apps:
    if app.slot_swap_status:
        print(app.name, app.slot_swap_status.timestamp_utc)

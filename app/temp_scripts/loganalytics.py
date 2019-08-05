from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.loganalytics import LogAnalyticsDataClient
from azure.loganalytics.models import QueryBody
import datetime, os
import numpy as np
from pandas import Series, DataFrame
import pandas as pd


tenant_id = os.environ.get('TENANT')
application_id = os.environ.get('CLIENT_ID_JENKINS')   
application_secret = os.environ.get('CLIENT_SECRET_JENKINS') 
subscription_id = os.environ.get('SUBSCRIPTION_ID')

workspace_id = '81af919a-92f9-4d81-8edf-041b4d81e278'

credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id,
    resource = 'https://api.loganalytics.io'
)

log_mgmt_client = LogAnalyticsManagementClient(credentials, subscription_id )


log_client = LogAnalyticsDataClient(credentials)

body = {"query": " AzureActivity | limit 1 ",
        "timespan": "P1M"}
query_result = log_client.query(workspace_id, body)


print(len(query_result.tables[0].columns))
import os

TENANT = os.environ.get('TENANT')
CLIENT_ID = os.environ.get('CLIENT_ID')
CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
CLIENT_ID_JENKINS = os.environ.get('CLIENT_ID_JENKINS')
CLIENT_SECRET_JENKINS = os.environ.get('CLIENT_SECRET_JENKINS')
SUBSCRIPTION_ID = os.environ.get('SUBSCRIPTION_ID')
PORT = 5000
AUTHORITY_HOST_URL = 'https://login.microsoftonline.com'
RESOURCE = 'https://management.azure.com'
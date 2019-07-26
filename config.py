import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    
    TENANT = os.environ.get('TENANT')
    CLIENT_ID = os.environ.get('CLIENT_ID')
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET')
    CLIENT_ID_JENKINS = os.environ.get('CLIENT_ID_JENKINS')
    CLIENT_SECRET_JENKINS = os.environ.get('CLIENT_SECRET_JENKINS')
    SUBSCRIPTION_ID = os.environ.get('SUBSCRIPTION_ID')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    PORT = 5000
    AUTHORITY_HOST_URL = 'https://login.microsoftonline.com'
    RESOURCE = 'https://management.azure.com'

    JIRA_USER = os.environ.get('JIRA_USER')
    JIRA_PASSWORD = os.environ.get('JIRA_PASSWORD')
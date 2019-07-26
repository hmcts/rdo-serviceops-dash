import os
import requests
from jira import JIRA
import re


# jira_user = app.config['JIRA_USER']
# jira_password = app.config['JIRA_PASSWORD']

jiraSession = requests.Session()

jira_user = os.environ.get('JIRA_USER')
jira_password = os.environ.get('JIRA_PASSWORD')

# options = {
#     'server': 'https://tools.hmcts.net/jira/'}

# jira = JIRA(options,basic_auth=('jira_user', 'jira_password'))

# projects = jira.projects()


# print(projects)



jira_session = requests.Session()
jira_url = "https://tools.hmcts.net/rest/api/2/serverInfo"
jira_user = os.environ.get('JIRA_USER')
jira_password = os.environ.get('JIRA_PASSWORD')

auth_values = (jira_user, jira_password)
headers={'content-type' : 'application/json'}
response = jira_session.post(jira_url, auth=auth_values, headers=headers)

print(response)
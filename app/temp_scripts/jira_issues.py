import os
import requests
import re
import json

jira_user = os.environ.get('JIRA_USER')
jira_password = os.environ.get('JIRA_PASSWORD')


jira_session = requests.Session()
jira_url = "https://tools.hmcts.net/jira/rest/api/2/serverInfo"

auth_values = (jira_user, jira_password)
headers={'content-type' : 'application/json'}
response = jira_session.get(jira_url, auth=auth_values, headers=headers)

json_data = response.json()

print(json_data)
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.alertsmanagement import AlertsManagementClient
import datetime, os, json, re

tenant_id = os.environ.get('TENANT')
application_id = os.environ.get('CLIENT_ID_JENKINS')   
application_secret = os.environ.get('CLIENT_SECRET_JENKINS') 
subscription_id = os.environ.get('SUBSCRIPTION_ID')

credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id
)

base_url = 'https://management.azure.com'

alerts_client = AlertsManagementClient(credentials, subscription_id, base_url)

alerts = alerts_client.alerts.get_all()

class Alert:
    def __init__(self, guid, name, state, severity, target_resource_name, target_resource_group, start_date, resolved_date):
        self.guid = guid,
        self.name = name,
        self.state = state,
        self.severity = severity,
        self.target_resource_name = target_resource_name,
        self.target_resource_group = target_resource_group,
        self.start_date = start_date,
        self.resolved_date = resolved_date

    @classmethod
    def from_json(cls, json_string):
        json_dict = json.loads(json_string)
        return cls(**json_dict)

    def __repr__(self):
        return f'<Alert { self.guid } { self.name } { self.severity } { self.resolved_date }>'

def get_alerts(alerts):

    for alert in alerts:
        regx = "/subscriptions/{}/providers/Microsoft.AlertsManagement/alerts/".format(subscription_id)
        alert_guid = re.sub(regx, '',alert.id)

        json_string = '{{\n "guid": "{}", \n "name": "{}", \n "state": "{}", \n "severity": "{}", \n "target_resource_name": "{}", \n "target_resource_group": "{}", \n "start_date": "{}", \n "resolved_date": "{}"\n }} '.format(
            alert_guid,
            alert.name, 
            alert.properties.essentials.alert_state,
            alert.properties.essentials.severity, 
            alert.properties.essentials.target_resource_name, 
            alert.properties.essentials.target_resource_group,
            alert.properties.essentials.start_date_time,
            alert.properties.essentials.monitor_condition_resolved_date_time
            )
        json_alert = Alert.from_json(json_string)
        print(json_string)


get_alerts(alerts)


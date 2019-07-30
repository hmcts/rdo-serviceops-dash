from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.alertsmanagement import AlertsManagementClient
import datetime, os

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

def get_alerts(alerts):

    for alert in alerts:
        print("Alert name: {} \n, Alert State {} \n, Alert Severity: {} \n, Target resource name {} \n, Target resource group: {} \n, Start date {}, \n Resolved Date {} \n".format(
            alert.name, 
            alert.properties.essentials.alert_state,
            alert.properties.essentials.severity, 
            alert.properties.essentials.target_resource_name, 
            alert.properties.essentials.target_resource_group,
            alert.properties.essentials.start_date_time,
            alert.properties.essentials.monitor_condition_resolved_date_time
            ))

get_alerts(alerts)
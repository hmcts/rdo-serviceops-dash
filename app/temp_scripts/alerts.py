
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.alertsmanagement import AlertsManagementClient
import datetime


tenant_id = '531ff96d-0ae9-462a-8d2d-bec7c0b42082'
application_id = 'f2279271-d0a0-45ed-ac1c-5aff1388ff01'   # devops_sandbox
application_secret = '.RS[03PGSl]*1A1L[gTs4+DTuLrkf3*n'   # devops_sandbox
subscription_id = 'bf308a5c-0624-4334-8ff8-8dca9fd43783'

credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id
)

base_url = 'https://management.azure.com'

alerts_client = AlertsManagementClient(credentials, subscription_id, base_url)

alerts = alerts_client.alerts.get_all()

day_ago = datetime.datetime.now() - datetime.timedelta(days = 1)


def get_alerts(alerts,severity="Sev0"):

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
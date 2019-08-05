from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.containerservice import ContainerServiceClient
from azure.mgmt.containerinstance import ContainerInstanceManagementClient
import os

tenant_id = os.environ.get('TENANT')
application_id = os.environ.get('CLIENT_ID_JENKINS')   
application_secret = os.environ.get('CLIENT_SECRET_JENKINS') 
subscription_id = 'b72ab7b7-723f-4b18-b6f6-03b0f2c6a1bb' # os.environ.get('SUBSCRIPTION_ID')

credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id,
)

container_client = ContainerServiceClient(credentials, subscription_id)
instance_client = ContainerInstanceManagementClient(credentials, subscription_id)

clusters = container_client.managed_clusters.list()

for cluster in clusters:
    print(cluster)

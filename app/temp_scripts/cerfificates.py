from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.keyvault import KeyVaultManagementClient
from azure.keyvault import KeyVaultClient
from azure.keyvault.models import *
import os, re, datetime

tenant_id = os.environ.get('TENANT')
application_id = os.environ.get('CLIENT_ID_JENKINS')   
application_secret = os.environ.get('CLIENT_SECRET_JENKINS') 
subscription_id = os.environ.get('SUBSCRIPTION_ID')

credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id,
)

kv_credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id,
    resource = "https://vault.azure.net"
)

kv_mgmt_client = KeyVaultManagementClient(credentials, subscription_id)
kv_client = KeyVaultClient(kv_credentials)

vaults = kv_mgmt_client.vaults.list()

expiry_date = datetime.datetime.now() + datetime.timedelta(days = 30)

for vault in vaults:
    vault_base_url = "https://{}.vault.azure.net".format(vault.name)
    certs = kv_client.get_certificates(vault_base_url)
    for cert in certs:
        regx = "{}/certificates/".format(vault_base_url)
        cert_name = re.sub(regx, '', cert.id)
        if cert.attributes.enabled == True and cert.attributes.expires.replace(tzinfo=None) < expiry_date:
            print("Cert {} in {} expires on {}".format(cert_name,vault.name,cert.attributes.expires))
import os
import adal 
import datetime

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.monitor import MonitorManagementClient

import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np


tenant_id = os.environ.get('TENANT')
application_id = os.environ.get('CLIENT_ID')   
application_secret = os.environ.get('CLIENT_SECRET')  
subscription_id = os.environ.get('SUBSCRIPTION_ID')

credentials = ServicePrincipalCredentials(
    client_id = application_id,
    secret = application_secret,
    tenant = tenant_id
)

# AZURE 
resource_client = ResourceManagementClient(credentials, subscription_id)
monitor_client = MonitorManagementClient(credentials, subscription_id)
sql_client = PostgreSQLManagementClient(credentials, subscription_id)
databases = sql_client.servers.list()

# TIMESPAN
now = datetime.datetime.now().time()
hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 1)
day_ago = datetime.datetime.now() - datetime.timedelta(days = 1)


def get_metric(metric,aggregation):

    metric_data = monitor_client.metrics.list(
        resource_id,
        timespan="{}/{}".format(day_ago, now),
        interval='PT15M',
        metricnames=metric,
        aggregation=aggregation
    )
    return metric_data


def get_timeseries_avg_data(metric_data,threshhold,metric_name):

    x_values, y_values = [], []

    for item in metric_data.value:
        for timeserie in item.timeseries:
            for data in timeserie.data:

                x_metrics, y_metrics = [], []
                x_values.append("".join(str(data.average)))
                y_values.append("".join(str(data.time_stamp)))
                
        x_metrics.extend(x_values)
        y_metrics.extend(y_values)

        return x_metrics, y_metrics, metric_name


def create_graph(cpu_metrics, storage_metrics):

    cpu = go.Scatter(
        x = cpu_metrics[1],
        y = cpu_metrics[0],
        mode = 'lines',
        name = cpu_metrics[2]
    )

    storage = go.Scatter(
        x = storage_metrics[1],
        y = storage_metrics[0],
        mode = 'lines',
        name = storage_metrics[2]
    )

    data = [cpu, storage] 
    layout = go.Layout(
        title = 'Usage for {} Database'.format(resource.name)
    )   
    fig = go.Figure(data=data,layout=layout)
    pyo.plot(fig, filename='graph.html')


for resource in databases:
    
    resource_id = resource.id
    cpu_usage = get_metric('cpu_percent','Average')
    storage_usage = get_metric('storage_percent','Average')
    cpu_metrics = get_timeseries_avg_data(cpu_usage, 10, 'CPU percent (Avg)')
    storage_metrics = get_timeseries_avg_data(storage_usage, 10, 'Storage percent (Avg)')

    create_graph(cpu_metrics,storage_metrics)

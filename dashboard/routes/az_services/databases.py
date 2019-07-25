from flask import Flask, Blueprint, render_template, request, flash
import os
import adal
import requests
import json
import datetime

from . import config

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.rdbms.postgresql import PostgreSQLManagementClient
from azure.mgmt.monitor import MonitorManagementClient

import plotly.offline as pyo
import plotly.graph_objs as go
import numpy as np


azdb = Blueprint('azdb', __name__)

@azdb.route('/azure_services/databases', methods=['GET', 'POST'])
def azure_dbs():

    tenant_id = config.TENANT
    application_id = config.CLIENT_ID_JENKINS
    application_secret = config.CLIENT_SECRET_JENKINS
    subscription_id = config.SUBSCRIPTION_ID

    credentials = ServicePrincipalCredentials(
        client_id=application_id,
        secret=application_secret,
        tenant=tenant_id
    )

    resource_client = ResourceManagementClient(credentials, subscription_id)
    sql_client = PostgreSQLManagementClient(credentials, subscription_id)
    monitor_client = MonitorManagementClient(credentials, subscription_id)

    now = datetime.datetime.now().time()
    hour_ago = datetime.datetime.now() - datetime.timedelta(hours = 1)
    day_ago = datetime.datetime.now() - datetime.timedelta(days = 1)

    databases = sql_client.servers.list()
    resources = sql_client.servers.list()

    def get_metric(resourceid,metric,aggregation):

        metric_data = monitor_client.metrics.list(
            resource_uri=resourceid,
            timespan="{}/{}".format(day_ago, now),
            interval='PT15M',
            metricnames=metric,
            aggregation=aggregation
        )
        return metric_data

    def get_timeseries_current_value(metric_data):

        x_values, y_values = [], []

        for item in metric_data.value:
            for timeserie in item.timeseries:
                for data in timeserie.data:

                    current_value = data.average
                    return current_value

    def get_timeseries_avg_data(metric_data):

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
    

    # for database in databases:
    #     resourceid = database.id
    #     cpu_usage = get_metric(resourceid,'cpu_percent','Average')
    #     # storage_usage = get_metric(resourceid,'storage_percent','Average')

    #     # cpu_metrics = get_timeseries_avg_data(cpu_usage, 10, 'CPU percent (Avg)')
    #     # storage_metrics = get_timeseries_avg_data(storage_usage, 10, 'Storage percent (Avg)')



    if request.method == 'POST':
        requested_database = request.form["databases"]
        
        cpu_usage = get_metric(requested_database,'cpu_percent','Average')
        current_value = get_timeseries_current_value(cpu_usage)

        message = current_value
        flash(message)

    return render_template('az_services/databases.html', databases=databases)


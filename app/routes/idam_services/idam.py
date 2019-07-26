from flask import Flask, Blueprint, render_template

import os
import adal
import requests
import json

from azure.common.credentials import ServicePrincipalCredentials

from . import config

idam = Blueprint('idam', __name__)

@idam.route('/idam_services')
def idam_services():

    return render_template('idam_services/index.html')

# ASA-FTD object parser
# fdm_deploy_functions.py - Deploy FDM config
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def deployfdm(fdm):
    url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/operational/deploy"

    payload = {}

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

    return response


def checkdeployment(fdm, deployment_id):
    url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/operational/deploy/"+deployment_id

    payload = {}

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("GET", url, headers=headers, data=payload, verify=False).json()

    return response

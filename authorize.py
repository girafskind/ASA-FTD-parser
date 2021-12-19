# authorize.py - Authorization against FxOS
# Version 0.1
# By Bo V Mortensen

import requests
import config
import json
import datetime
from requests.auth import HTTPBasicAuth

def fdmgettoken(fdm):
    url = "https://{}:{}/api/fdm/v6/fdm/token".format(fdm.ip, fdm.port)

    payload = '{{"grant_type": "password","username": "{}","password": "{}"}}'.format(fdm.username, fdm.password)

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
    now = datetime.datetime.now()

    fdm.access_token = response['access_token']
    fdm.refresh_token = response['refresh_token']
    fdm.expires = now + datetime.timedelta(seconds=response['expires_in'])
    fdm.refresh_expires = now + datetime.timedelta(seconds=response['refresh_expires_in'])
    return response

def fxosgettoken(ftd):
    url = "https://" + ftd.ip + ":" + ftd.port + "/api/login"

    auth = HTTPBasicAuth(ftd.username, ftd.password)

    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'User-agent': 'REST API Agent',
      'username': ftd.username,
      'password': ftd.password
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).text
    config.FXOSTOKEN = json.loads(response)

    return response

def fxoslogout(ftd):
    url = "https://" + ftd.ip + ":" + ftd.port + "/api/login"

    payload = {}

    headers = {
        'Authorization': 'Bearer '+str(ftd.token['token']),
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).text

    return response

def asagettoken(asa):
    url = "https://" + asa.ip + ":" + asa.port + "/api/tokenservices"

    basicauth = HTTPBasicAuth(asa.username, asa.password)

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent'
    }

    response = requests.request("POST", url, auth=basicauth, headers=headers, data=payload, verify=False)

    return response.headers['X-Auth-Token']

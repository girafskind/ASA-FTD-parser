# ASA-FTD object parser
# authorize.py - Authorization against ASA and FDM
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

import requests
import datetime
from requests.auth import HTTPBasicAuth

def fdm_get_token(fdm):
    """
    This function gets an API token from the given FDM object, it will add the values to the FDM object.
    :param fdm: FDM object which will create a token
    :return: Returns the HTTP response from the FDM
    """
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


def asa_get_token(asa):
    """
    This function gets an API token from the given ASA object.
    :param asa: ASA object which will create a token
    :return: Returns an X-Auth-Token
    """
    url = "https://" + asa.ip + ":" + asa.port + "/api/tokenservices"

    basicauth = HTTPBasicAuth(asa.username, asa.password)

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent'
    }

    response = requests.request("POST", url, auth=basicauth, headers=headers, data=payload, verify=False)

    return response.headers['X-Auth-Token']


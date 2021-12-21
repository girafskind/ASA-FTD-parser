# ASA-FTD object parser
# authorize.py - Authorization against ASA and FDM
# Version 1.0
# By Bo V Mortensen
# 20th December 2021
import sys

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

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            print("Got HTTP error 400, bad request or login credentials")
        sys.exit()
    except requests.exceptions.ConnectionError as errc:
        print("An error connecting to API occurered: " + repr(errc))
        sys.exit()
    except requests.exceptions:
        print("Something else happened")
        sys.exit()

    now = datetime.datetime.now()
    json_response = response.json()
    fdm.access_token = json_response['access_token']
    fdm.refresh_token = json_response['refresh_token']
    fdm.expires = now + datetime.timedelta(seconds=json_response['expires_in'])
    fdm.refresh_expires = now + datetime.timedelta(seconds=json_response['refresh_expires_in'])
    return json_response


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

    try:
        response = requests.request("POST", url, auth=basicauth, headers=headers, data=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            print("Got HTTP error 400, bad request or login credentials")
        sys.exit()
    except requests.exceptions.ConnectionError as errc:
        print("An error connecting to API occurered: " + repr(errc))
        sys.exit()
    except requests.exceptions:
        print("Something else happened")
        sys.exit()

    return response.headers['X-Auth-Token']

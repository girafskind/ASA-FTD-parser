# ASA-FTD object parser
# asa_networkservice_functions.py - collection of network services functions
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def get_number_of_asa_service_objects(asa):
    """
    Returns the number of service objects the given ASA object has configured.
    :param asa: ASA device to count network objects.
    :return: Integer which describes how many objects is found on ASA.
    """
    url = asa.url() + "/api/objects/networkservices?limit=1"

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response['rangeInfo']['total']


def get_number_of_asa_service_groups(asa):
    """
    Returns the number of service object-groups the given ASA object has configured.
    :param asa: ASA device to count network object-groups.
    :return: Integer which describes how many object-groups is found on ASA.
    """
    url = asa.url() + "/api/objects/networkservicegroups?limit=1"

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response['rangeInfo']['total']


def get_all_service_objects(asa):
    """
    This functions retreives all service-objects.
    :param asa: ASA device which to retrieve the objects from ASA
    :return: Returns list of service objects.
    """
    url = asa.url() + "/api/objects/networkservices"

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()['items']

    return response


def get_all_service_groups(asa):
    """
    This function retrieves all service groups from ASA
    :param asa: ASA device which to retrieve the objects from ASA
    :return: Returns list of service objects.
    """
    url = asa.url() + "/api/objects/networkservicegroups"

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()['items']

    return response

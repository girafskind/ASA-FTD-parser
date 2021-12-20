# ASA-FTD object parser
# asa_object_functions.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Functions towards Cisco ASA

import requests
from Services import fdm_object_functions


def parse_asa_network_groups(fdm, netgroups):
    """
    This function takes all network-group objects, then pushes them one after one to the given FDM object.
    """
    for group in netgroups:
        fdm_object_functions.create_fdm_network_group(fdm, group)


def get_number_of_network_objects(asa):
    """
    Returns the number of network objects the given ASA object has configured.
    :param asa: ASA device to count network objects.
    :return: Integer which describes how many objects is found on ASA.
    """
    url = "https://" + asa.ip + ":" + asa.port + "/api/objects/networkobjects?limit=1"

    objects = {}

    payload = {}

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response['rangeInfo']['total']


def get_number_of_network_groups(asa):
    """
    Returns the number of network object-groups the given ASA object has configured.
    :param asa: ASA device to count network object-groups.
    :return: Integer which describes how many object-groups is found on ASA.
    """
    url = "https://" + asa.ip + ":" + asa.port + "/api/objects/networkobjectgroups?limit=1"

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response['rangeInfo']['total']


def get_all_asa_network_objects(asa):
    """
    Returns all network objects present on the ASA, circumventing the limit of 100 objects.
    :param asa: The ASA which to retrieve objects from
    :return: All objects in a list
    """
    totalobjects = get_number_of_network_objects(asa)

    offset = 0
    asaobjects = []

    while offset < totalobjects:
        asaobjects.extend(get_asa_network_objects(asa, offset=offset))
        offset = offset + 100

    return asaobjects


def get_all_asa_network_groups(asa):
    """
    Returns all network object-groups present on the ASA, circumventing the limit of 100 objects.
    :param asa: The ASA which to retrieve object-groups from
    :return: All object-groups in a list
    """
    totalobjects = get_number_of_network_groups(asa)

    offset = 0
    asaobjects = []

    while offset < totalobjects:
        asaobjects.extend(get_asa_network_groups(asa, offset=offset))
        offset = offset + 100

    return asaobjects


def get_asa_network_objects(asa, limit=100, offset=0):
    """
    This function returns all network objects, give an ASA object as arguement.
    Offset value is the starting point, 0 is from first object.
    Limit is an integer between 1 and 100, this value decides how many objects is returned starting from offset-value.
    :param asa: ASA to get network objects from
    :param limit: How may objects should be returned, integer (1-100)
    :param offset: Which index to start from.
    :return: Returns <limit> ASA objects, starting from <limit>
    """
    url = "https://" + asa.ip + ":" + asa.port + "/api/objects/networkobjects?limit="+str(limit)+"&offset="+str(offset)

    payload = {
    }

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()['items']

    return response


def get_asa_network_groups(asa, limit=100, offset=0):
    """
    This function returns all network object-groups, give an ASA object as arguement.
    Offset value is the starting point, 0 is from first object.
    Limit is an integer between 1 and 100, this value decides how many object-groups,
    is returned starting from offset-value.
    :param asa: ASA to get network object-groups from
    :param limit: How may object-groups should be returned, integer (1-100)
    :param offset: Which index to start from.
    :return: Returns <limit> ASA object-groups, starting from <limit>
    """
    url = "https://" + asa.ip + ":" + asa.port + "/api/objects/networkobjectgroups?limit="+str(limit)+"&offset="+str(offset)

    payload = {
    }

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()['items']

    return response

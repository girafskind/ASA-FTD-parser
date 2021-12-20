# ASA-FTD object parser
# fdm_networkobject_functions.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Functions towards Cisco FDM

import requests
import json

def create_fdm_network_object(fdm, asanetobj):
    """
    This function creates an object on the FDM device, accepts all types of network objects:
    Host, subnet, FQDN or IP-address range.
    :param fdm: Receiving FDM object
    :param asanetobj: ASA network object
    :return: Response from FDM device
    """
    url = "https://"+fdm.ip+":"+fdm.port+"/api/fdm/v6/object/networks"

    object_type = ""

    if asanetobj['host']['kind'] == 'IPv4Network':
        object_type = "NETWORK"
    elif asanetobj['host']['kind'] == 'IPv4Address':
        object_type = "HOST"
    elif asanetobj['host']['kind'] == 'IPv4FQDN':
        object_type = "FQDN"
    elif asanetobj['host']['kind'] == 'IPv4Range':
        object_type = "RANGE"

    payload = json.dumps({
        "name": asanetobj['name'],
        "subType": object_type,
        "value": asanetobj['host']['value'],
        "type": "networkobject"
    })

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

    return response


def create_fdm_network_group(fdm, objectgroup):
    """
    This function creates an object-group on the FDM device.
    :param fdm: Receiving FDM object
    :param objectgroup: ASA network object-group
    :return: Response from FDM device
    """
    url = "https://"+fdm.ip+":"+fdm.port+"/api/fdm/v6/object/networkgroups"

    prepayload = {
        'name': objectgroup.get('objectId'),
        'type': 'networkobjectgroup',
        'objects': []
    }

    for groupmember in objectgroup.get('members'):
        prepayload['objects'].append(
            {'name': groupmember.get('objectId'),
             'type': 'networkobject'
             }
        )

    payload = json.dumps(prepayload)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

    return response

def get_fdm_objects(fdm):
    """
    Get all network objects on FDM
    :param fdm:
    :return: List containing all network objects
    """
    url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/object/networks"

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response


def get_fdm_object_groups(fdm):
    """
    Get all network object-groups on FDM
    :param fdm:
    :return: List containing all network object-groups
    """
    url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/object/networkgroups"

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()


def get_all_fdm_objects(fdm, limit=100, offset=0):
    """
    Get all network objects on FDM, limit=0 returns all objects
    :param fdm:
    :return: List containing all network objecs
    """
    url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/object/networks?offset="+str(offset)+"&limit="+str(limit)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response

def get_all_fdm_object_groups(fdm, limit=100, offset=0):
    """
    Get all network object-groups on FDM, limit=0 returns all object-groups
    :param fdm:
    :return: List containing all network object-groups
    """
    url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/object/networkgroups?offset="+str(offset)+"&limit="+str(limit)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response

def delete_all_fdm_objects(fdm):
    """
    Deletes all objects on FDM which does not have isSystemDefined=true
    :param fdm: FDM object
    :return: Nothing
    """
    all_objects = get_all_fdm_objects(fdm, limit=0)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    for network_object in all_objects['items']:
        network_object_id = network_object['id']
        url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/object/networks/" + network_object_id
        response = requests.request("DELETE", url, headers=headers, verify=False)

def delete_all_fdm_object_groups(fdm):
    """
    Deletes all object-groups on FDM which does not have isSystemDefined=true
    :param fdm: FDM object
    :return: Nothing
    """

    all_object_groups = get_all_fdm_object_groups(fdm, limit=0)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    for object_group in all_object_groups['items']:
        network_group_id = object_group['id']
        url = "https://" + fdm.ip + ":" + fdm.port + "/api/fdm/v6/object/networkgroups/"+network_group_id
        response = requests.request("DELETE", url, headers=headers, verify=False)


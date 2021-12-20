# ASA-FTD object parser
# fdm_functions.py
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

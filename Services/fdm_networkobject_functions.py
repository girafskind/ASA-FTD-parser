# ASA-FTD object parser
# fdm_networkobject_functions.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Functions towards Cisco FDM
import sys

import requests
import json
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def create_fdm_network_object(fdm, asanetobj, migration):
    """
    This function creates an object on the FDM device, accepts all types of network objects:
    Host, subnet, FQDN or IP-address range.
    :param fdm: Receiving FDM object
    :param asanetobj: ASA network object
    :param migration: Migration status class
    :return: Response from FDM device
    """
    url = fdm.url() + "/api/fdm/v6/object/networks"

    object_type = ""

    if asanetobj['host']['kind'] in ('IPv4Network', 'IPv6Network'):
        object_type = "NETWORK"
    elif asanetobj['host']['kind'] in ('IPv4Address', 'IPv6Address'):
        object_type = "HOST"
    elif asanetobj['host']['kind'] in ('IPv4FQDN', 'IPv6FQDN'):
        object_type = "FQDN"
    elif asanetobj['host']['kind'] in ('IPv4Range', 'IPv6Range'):
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

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            print("Got HTTP error 400, bad request or login credentials")
        if response.status_code == 422:
            print("Got HTTP error 422, duplicate element: " + payload)
            reason = json.loads(response.content)['error']['messages'][0]['description']
            migration.add_duplicate_network(payload, reason)
            return
        sys.exit()
    except requests.exceptions.ConnectionError as errc:
        print("An error connecting to API occurered: " + repr(errc))
        sys.exit()
    except requests.exceptions:
        print("Something else happened")
        sys.exit()

    migration.add_migrated_net()

    return response.json()


def create_fdm_network_group(fdm, objectgroup, migration):
    """
    This function creates an object-group on the FDM device.
    :param fdm: Receiving FDM object
    :param objectgroup: ASA network object-group
    :param migration: Migration status class
    :return: Response from FDM device
    """
    url = fdm.url() + "/api/fdm/v6/object/networkgroups"

    prepayload = {
        'name': objectgroup.get('objectId'),
        'type': 'networkobjectgroup',
        'objects': []
    }

    for groupmember in objectgroup.get('members'):
        converted_group_member = check_object_group_for_ip_values(groupmember, fdm, migration)
        prepayload['objects'].append(
            {'name': converted_group_member.get('objectId'),
             'type': 'networkobject'
             }
        )

    payload = json.dumps(prepayload)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            print("Got HTTP error 400, bad request or login credentials")
        if response.status_code == 422:
            reason = json.loads(response.content)['error']['messages'][0]['description']
            migration.add_duplicate_network(payload, reason)
            return
        sys.exit()
    except requests.exceptions.ConnectionError as errc:
        print("An error connecting to API occurered: " + repr(errc))
        sys.exit()
    except requests.exceptions:
        print("Something else happened")
        sys.exit()

    migration.add_migrated_group()

    return response.json()


def get_fdm_objects(fdm):
    """
    Get all network objects on FDM
    :param fdm:
    :return: List containing all network objects
    """
    url = fdm.url() + "/api/fdm/v6/object/networks"

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
    url = fdm.url() + "/api/fdm/v6/object/networkgroups"

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()

    return response


def get_all_fdm_objects(fdm, limit=100, offset=0):
    """
    Get all network objects on FDM, limit=0 returns all objects
    :param fdm: FDM object
    :param limit: Integer 0-100, how many objects to return
    :param offset: Integer, starting point of objects
    :return: List containing all network objecs
    """
    url = fdm.url() + "/api/fdm/v6/object/networks?offset=" + str(offset) + "&limit=" + str(limit)

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
    :param limit: Integer 0-100, how many objects to return
    :param offset: Integer, starting point of objects
    :return: List containing all network object-groups
    """
    url = fdm.url() + "/api/fdm/v6/object/networkgroups?offset=" + str(offset) + "&limit=" + str(limit)

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
        url = fdm.url() + "/api/fdm/v6/object/networks/" + network_object_id
        response = requests.request("DELETE", url, headers=headers, verify=False)

    return response


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
        url = fdm.url() + "/api/fdm/v6/object/networkgroups/" + network_group_id
        response = requests.request("DELETE", url, headers=headers, verify=False)

    return response


def check_object_group_for_ip_values(group_object, fdm, migration):
    """
    Check if network group-object contains IP host addresses or subnets, creates them as objects if they do.
    :param group_object: ASA network object-group
    :param fdm: The FDM device to create the missing object
    :param migration: The migration status object
    :return:
    """

    if group_object['kind'] == "IPv4Network":
        asanetobj = {
            'name': 'Obj-' + group_object['value'].replace('/', '-'),
            'objectId': 'Obj-' + group_object['value'].replace('/', '-'),
            'host': {
                'kind': group_object['kind'],
                'value': group_object['value']
            }
        }

        create_fdm_network_object(fdm, asanetobj, migration)
        return asanetobj

    if group_object['kind'] == "IPv4Address":
        asanetobj = {
            'name': 'Obj-' + group_object['value'],
            'objectId': 'Obj-' + group_object['value'].replace('/', '-'),
            'host': {
                'kind': group_object['kind'],
                'value': group_object['value']
            }
        }

        create_fdm_network_object(fdm, asanetobj, migration)
        return asanetobj

    return group_object

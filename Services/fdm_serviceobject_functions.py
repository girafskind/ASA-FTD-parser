# ASA-FTD object parser
# fdm_serviceobject_functions.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Functions towards Cisco FDM

import json
import sys
import requests.exceptions
from Services import named_ports_translator, icmp_translator
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def parse_asa_portvalue(asaserviceobj):
    """
    Translate the value of ASA service object and seperates port number and protocol.
    :param asaserviceobj:
    :return: Dictionary of port and protocol
    """
    service_dict = {}

    if asaserviceobj['kind'] == "object#TcpUdpServiceObj":
        protocol, port = asaserviceobj['value'].split("/")

        if not port.isnumeric():
            port = named_ports_translator.no_port_names(port)

        service_dict = {
            "name": asaserviceobj['name'],
            "type": protocol + "portobject",
            "port": port,
            "url-tail": protocol + "ports"
        }
    elif asaserviceobj['kind'] == "object#NetworkProtocolObj":
        service_dict = {
            "name": asaserviceobj['name'],
            "type": "protocolobject",
            "protocol": asaserviceobj['value'].upper(),
            "url-tail": "protocols"
        }
    elif asaserviceobj['kind'] == 'object#ICMPServiceObj':

        icmp_for_fdm = icmp_translator.translate_icmp(asaserviceobj)

        service_dict = {
            "name": asaserviceobj['name']
        }
        service_dict.update(icmp_for_fdm)

    return service_dict


def create_fdm_port_object(fdm, asaserviceobj, migration):
    """
    This function create an FDM port object.
    :param fdm: Target FDM
    :param asaserviceobj: Service object in JSON from ASA
    :param migration: Migration status object
    :return:
    """

    port_type_dict = parse_asa_portvalue(asaserviceobj)

    url = fdm.url() + "/api/fdm/v6/object/" + port_type_dict['url-tail']

    port_type_dict.pop('url-tail')
    payload = json.dumps(port_type_dict)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.status_code == 400:
            print("Got HTTP error 400, bad request or login credentials")
        if response.status_code == 404:
            print("Got HTTP error 404, not found")
        if response.status_code == 422:
            reason = json.loads(response.content)['error']['messages'][0]['description']
            migration.add_duplicate_service(payload, reason)
            return
        else:
            print("HTTP error:" + str(err))
            sys.exit()
    except requests.exceptions.ConnectionError as errc:
        print("An error connecting to API occurered: " + repr(errc))
        sys.exit()
    except requests.exceptions:
        print("Something else happened")
        sys.exit()

    migration.add_migrated_service()
    return response.json()


def create_fdm_port_group(fdm, asa_service_group):
    """
    This function creates a service group
    :param fdm: The target FDM
    :param asaservicegroup: The ASA service group
    :param migration: Migration status
    :return:
    """

    payload = {
        'name' : asa_service_group['name']
    }

    for service in asa_service_group['members']:
        print(service)

    url = fdm.url() + "/api/fdm/v6/object/portgroups"

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }
    print(asa_service_group)

    print(payload)
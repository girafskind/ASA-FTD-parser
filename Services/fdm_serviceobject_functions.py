# ASA-FTD object parser
# fdm_serviceobject_functions.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Functions towards Cisco FDM

import json

import requests.exceptions


def parse_asa_portvalue(asaserviceobj):
    """
    Translate the value of ASA service object and seperates port number and protocol.
    :param asaserviceobj:
    :return: Dictionary of port and protocol
    """
    if asaserviceobj['kind'] == "object#TcpUdpServiceObj":
        protocol, port = asaserviceobj['value'].split("/")

        service_dict = {
            'protocol' : protocol,
            'port': port,
            'url-tail': protocol + "ports"
        }

        return service_dict


def create_fdm_port_object(fdm, asaserviceobj, migration):
    """
    This function create an FDM port object.
    :param fdm:
    :param asaserviceobj:
    :param migration:
    :return:
    """

    porttype = parse_asa_portvalue(asaserviceobj)

    url = fdm.url() + "/api/fdm/v6/object/" + porttype['url-tail']

    payload = json.dumps({
        "name": asaserviceobj['name'],
        "port": porttype['port'],
        "type": porttype['protocol'] + "portobject"
    })
    print(payload)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
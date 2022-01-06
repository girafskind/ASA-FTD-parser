# ASA-FTD object parser
# fdm_serviceobject_functions.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Functions towards Cisco FDM

import json
import sys
import requests.exceptions
from Services import asa_networkservice_functions
from Services import named_ports_translator, icmp_translator
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def parse_asa_service_group(asa_service_group):
    """
    Parses the service group members from the ASA to FDM syntax
    :param asa_service_group: The ASA service group.
    :return: FDM syntax group member
    """

    if asa_service_group['kind'] == "object#TcpUdpServiceObj":
        pass

    elif asa_service_group['kind'] == "object#NetworkProtocolObj":
        member_dict = {
            'type': 'protocolobject',
            'name': asa_service_group['value']
        }

        return member_dict

    elif asa_service_group['kind'] == "object#ICMPServiceObj":
        pass
    elif asa_service_group['kind'] == "object#ICMP6ServiceObj":
        pass

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
    elif asaserviceobj['kind'] == "object#NetworkProtocolObj" and asaserviceobj['value'] == "icmp":
        icmp_for_fdm = icmp_translator.translate_icmp(asaserviceobj)

        service_dict = {
            "name": asaserviceobj['name'],
            "url-tail": "icmpv4ports"
        }
        service_dict.update(icmp_for_fdm)
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
            "name": asaserviceobj['name'],
            "url-tail": "icmpv4ports"
        }
        service_dict.update(icmp_for_fdm)
    elif asaserviceobj['kind'] == 'object#ICMP6ServiceObj':

        icmp_for_fdm = icmp_translator.translate_icmp(asaserviceobj)

        service_dict = {
            "name": asaserviceobj['name'],
            "url-tail": "icmpv6ports"
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
            print("Got HTTP error 422, duplicate element: " + payload)
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


def create_fdm_port_group(fdm, asa, asa_service_group, migration):
    """
    This function creates a service group
    :param fdm: The target FDM
    :param asa: The source ASA
    :param asa_service_group: The ASA service group
    :param migration: Migration status
    :return:
    """
    url = fdm.url() + "/api/fdm/v6/object/portgroups"

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    prepayload = {
        'name' : 'Service_group_' + asa_service_group['name'],
        'type': 'portobjectgroup',
        'objects': []
    }

    for service in asa_service_group['members']:
        if service['kind'] == "objectRef#TcpUdpServiceObj":
            service_protocol = asa_networkservice_functions.clarify_tcp_udp_service(service, asa)
            prepayload['objects'].append(
                {
                    'name': service['objectId'],
                    'type': service_protocol
                }
            )
        elif service['kind'] == "NetworkProtocol" and service['value'] != "icmp":
            synthetic_asa_object = {
                'kind': 'object#NetworkProtocolObj',
                'name': service['value'].upper(),
                'value': service['value']
            }

            create_fdm_port_object(fdm, synthetic_asa_object, migration)

            prepayload['objects'].append(
                {
                    'name': service['value'].upper(),
                    'type': 'protocolobject'
                }
            )
        elif service['kind'] == "NetworkProtocol" and service['value'] == "icmp":
            synthetic_asa_object = {
                'kind': 'object#ICMPServiceObj',
                'name': 'icmp',
                'value': 'icmp'
            }

            create_fdm_port_object(fdm, synthetic_asa_object, migration)

            prepayload['objects'].append(
                {
                    'name': service['value'].upper(),
                    'type': 'icmpv4portobject'
                }
            )
        elif service['kind'] == "TcpUdpService" and service['value'].split("/")[0] != "tcp-udp":
            name_list = service['value'].split("/")
            synthetic_asa_object = {
                'kind': "object#TcpUdpServiceObj",
                'name': name_list[0] + "_" + name_list[1],
                'value': service['value']
            }

            create_fdm_port_object(fdm, synthetic_asa_object, migration)
            prepayload['objects'].append(
                {
                    'name': name_list[0] + "_" + name_list[1],
                    'type': name_list[0] + "portobject"
                }
            )
        elif service['kind'] == "ICMPService":
            icmp_type = service['value'].split("/")[0]
            icmp_code = service['value'].split("/")[1]

            synthetic_asa_object = {
                'kind': "object#ICMPServiceObj",
                'name': icmp_type + "-" + icmp_code,
                'value': service['value']
            }

            create_fdm_port_object(fdm, synthetic_asa_object, migration)
            prepayload['objects'].append(
                {
                    'name': icmp_type + '-' + icmp_code,
                    'type': 'icmpv4portobject'
                }
            )

        elif service['kind'] == "TcpUdpService" and service['value'].split("/")[0] == "tcp-udp":
            name_list = []
            name_list.append(service['value'].split("/")[0].split("-")[0]+"/"+service['value'].split("/")[1])
            name_list.append(service['value'].split("/")[0].split("-")[1] + "/" + service['value'].split("/")[1])

            for name in name_list:
                synthetic_asa_object = {
                    'kind': "object#TcpUdpServiceObj",
                    'name': name.replace("/","-"),
                    'value': name
                }

                create_fdm_port_object(fdm, synthetic_asa_object, migration)
                prepayload['objects'].append(
                    {
                        'name': name.replace("/", "-"),
                        'type': name.split("/")[0] + "portobject"
                    }
                )

    payload = json.dumps(prepayload)

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

    migration.add_migrated_service_group()

    return response.json()

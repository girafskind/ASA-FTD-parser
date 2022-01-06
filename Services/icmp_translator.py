# ASA-FTD object parser
# icmp_translator.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Parsing ICMP types and codes

import json


def translate_icmp(icmp_input):
    with open("JSON/icmp-types.JSON", "r") as json_icmp:
        icmp_dict = json.load(json_icmp)

    icmp_value = icmp_input['value'].split("/")

    icmp_object = {"icmpv4Code": None}

    if icmp_input['kind'] == 'object#ICMPServiceObj' or icmp_input['kind'] == "object#NetworkProtocolObj":
        if len(icmp_value) == 1:
            icmp_object['icmpv4Type'] = 'ANY'
        else:
            icmp_object['icmpv4Type'] = icmp_dict['ipv4'][icmp_value[1]]['fdm-name']
        icmp_object['type'] = 'icmpv4portobject'
        if len(icmp_value) == 3:
            icmp_object['icmpv4Code'] = icmp_dict['ipv4'][icmp_value[1]]['codes'][icmp_value[2]]
        elif len(icmp_value) == 2:
            icmp_object['icmpv4Type'] = icmp_dict['ipv4'][icmp_value[1]]['fdm-name']
    elif icmp_input['kind'] == 'object#ICMP6ServiceObj':
        icmp_object['icmpv6Type'] = icmp_dict['ipv6'][icmp_value[1]]['fdm-name']
        icmp_object['type'] = 'icmpv6portobject'
        if len(icmp_value) == 3:
            icmp_object['icmpv6Code'] = icmp_dict['ipv6'][icmp_value[1]]['codes'][icmp_value[2]]
        elif len(icmp_value) == 2:
            icmp_object['icmpv6Type'] = icmp_dict['ipv6'][icmp_value[1]]['fdm-name']


    return icmp_object


icmp_test_object_1 = {
      "kind": "object#ICMPServiceObj",
      "selfLink": "https://192.168.2.16:4443/api/objects/networkservices/ICMP-TEST",
      "name": "ICMP-TEST",
      "value": "icmp/echo",
      "objectId": "ICMP-TEST"
    }

icmp_test_object_2 = {
      "kind": "object#ICMPServiceObj",
      "name": "icmp",
      "value": "icmp"
    }


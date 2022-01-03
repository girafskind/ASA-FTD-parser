# ASA-FTD object parser
# icmp_translator.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Parsing ICMP types and codes

import json


def translate_icmp(icmp_object):
    with open("JSON/icmp-types.JSON", "r") as json_icmp:
        icmp_dict = json.load(json_icmp)

    icmp_value = icmp_object['value'].split("/")
    icmp_code = ""

    if icmp_object['kind'] == 'object#ICMPServiceObj':
        icmp_type = icmp_dict['ipv4'][icmp_value[1]]
        if len(icmp_type) == 3:
            icmp_code = icmp_dict['ipv4'][icmp_value[1]]
    elif icmp_object['kind'] == 'object#ICMP6ServiceObj':
        pass

    print(icmp_type)
    print(icmp_code)


icmp_object =  {
      "kind": "object#ICMPServiceObj",
      "selfLink": "https://192.168.2.16:4443/api/objects/networkservices/ICMP-TEST",
      "name": "ICMP-TEST",
      "value": "icmp/unreachable/8",
      "objectId": "ICMP-TEST"
    }

translate_icmp(icmp_object)

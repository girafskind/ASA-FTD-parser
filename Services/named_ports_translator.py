# ASA-FTD object parser
# named_ports_translator.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021
# Parsing named ports in ASA config to regular port numbers

import json


def no_port_names(name):
    with open("JSON/named-ports.JSON", "r") as json_ports:
        ports = json.load(json_ports)

    if name in ports:
        return ports[name]
    else:
        return name


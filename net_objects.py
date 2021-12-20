# ASA-FTD object parser
# net_objects.py
# By Bo V Mortensen
# Version 1.0
# 20th December 2021

# Get network objects from asa
import http

import requests
import json

def getallasanetworkobjects(asa):
    totalobjects = getnumberofnetworkobjects(asa)

    offset = 0
    asaobjects = []

    while offset < totalobjects:
        asaobjects.extend(getasanetworkobjects(asa, offset=offset))
        offset = offset + 100

    return asaobjects

def getnumberofnetworkobjects(asa):
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


def getasanetworkobjects(asa, limit=100, offset=0):
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

def createfdmnetworkobject(fdm,object):
    url = "https://"+fdm.ip+":"+fdm.port+"/api/fdm/v6/object/networks"

    object_type = ""

    if object['host']['kind'] == 'IPv4Network':
        object_type = "NETWORK"
    elif object['host']['kind'] == 'IPv4Address':
        object_type = "HOST"
    elif object['host']['kind'] == 'IPv4FQDN':
        object_type = "FQDN"
    elif object['host']['kind'] == 'IPv4Range':
        object_type = "RANGE"

    payload = json.dumps({
        "name": object['name'],
        "subType": object_type,
        "value": object['host']['value'],
        "type": "networkobject"
    })

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()

    return response
# ASA-FTD object parser
# net_objects.py
# By Bo Vittus Mortensen
# Version 0.1

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
    #print(url)

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
    #print(url)
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

    print(payload)

    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + fdm.access_token
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False).json()
    print(response)
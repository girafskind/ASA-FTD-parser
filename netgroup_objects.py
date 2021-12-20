# ASA-FTD object parser
# netgroup_objects.py
# By Bo Vittus Mortensen
# Version 0.1

# Get network objects-groups from asa
import requests
import json


def getallasanetworkgroups(asa):
    totalobjects = getnumberofnetworkgroups(asa)

    offset = 0
    asaobjects = []

    while offset < totalobjects:
        asaobjects.extend(getasanetworkgroups(asa, offset=offset))
        offset = offset + 100

    return asaobjects

def getnumberofnetworkgroups(asa):
    url = "https://" + asa.ip + ":" + asa.port + "/api/objects/networkobjectgroups?limit=1"
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


def getasanetworkgroups(asa, limit=100, offset=0):
    url = "https://" + asa.ip + ":" + asa.port + "/api/objects/networkobjectgroups?limit="+str(limit)+"&offset="+str(offset)
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


def parseasanetgroups(fdm, netgroups):

    for group in netgroups:
        createfdmnetworkgroup(fdm, group)


def createfdmnetworkgroup(fdm, objectgroup):
    url = "https://"+fdm.ip+":"+fdm.port+"/api/fdm/v6/object/networkgroups"

    prepayload = {
        'name': objectgroup.get('objectId'),
        'type': 'networkobjectgroup',
        'objects': []
    }

    for groupmember in objectgroup.get('members'):
        #print("new object")
        #print(groupmember)
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
    print(response)
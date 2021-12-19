# ASA-FTD object parser
# netgroup_objects.py
# By Bo Vittus Mortensen
# Version 0.1

# Get network objects-groups from asa
import requests


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
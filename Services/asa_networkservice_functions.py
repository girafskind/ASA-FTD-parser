# ASA-FTD object parser
# asa_networkservice_functions.py - collection of network services functions
# Version 1.0
# By Bo V Mortensen
# 20th December 2021


import requests


def get_number_of_service_objects(asa):
    pass


def get_all_service_objects(asa):
    """
    This functions retreives all service-objects.
    :param asa: ASA device which to retreive the objects from
    :return: Returns list of service objects.
    """
    url = asa.url() + "/api/objects/networkservices"

    headers = {
        'Content-Type': 'application/json',
        'User-agent': 'REST API Agent',
        'X-Auth-Token': asa.token
    }

    response = requests.request("GET", url, headers=headers, verify=False).json()['items']

    return response

def get_all_service_groups(asa):
    pass
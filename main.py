# ASA-FTD object parser
# main.py - Main program
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

from Services import fdm_functions, asa_functions, fdm_deploy_functions
from Classes import Devices
import authorize
import config


def main():
    """
    Main function which initialized one ASA and one FDM object, from the credentials entered in the config.py file.
    Then parse all objects on the ASA to the FDM.
    """
    fdm1 = initialize_fdm()
    asa1 = initialize_asa()

    parse_objects(asa1, fdm1)


def parse_objects(asa, fdm):
    """
    Function which first get all objects from ASA as a list, then creates them on the FDM.
    Then gets all object-groups from ASA as a list, then creates them on the FDM.
    An object-group cannot contain a object which does not exist.
    :param asa: Soruce ASA
    :param fdm: Destination FDM
    :return: Nothing
    """
    asa_objects = asa_functions.get_all_asa_network_objects(asa)
    for asa_object in asa_objects:
        fdm_functions.create_fdm_network_object(fdm, asa_object)

    asanetgroups = asa_functions.get_all_asa_network_groups(asa)
    for group in asanetgroups:
        fdm_functions.create_fdm_network_group(fdm, group)


def initialize_fdm():
    """
    Initialize a FDM object from info entered in config.py
    :return: A FDM object, containing an access- and refresh-token.
    """
    newfdm = Devices.FTDClass()
    newfdm.ip = config.ftdip
    newfdm.username = config.ftdusername
    newfdm.password = config.ftdpassword
    authorize.fdm_get_token(newfdm)

    return newfdm


def initialize_asa():
    """
    Initialize a ASA object from info entered in config.py
    :return: A ASA object, containing an access-token.
    """
    newasa = Devices.ASAClass()
    newasa.ip = config.asaip
    newasa.username = config.asausername
    newasa.password = config.asapassword
    newasa.port = config.asaport
    newasa.token = authorize.asa_get_token(newasa)

    return newasa


def deploy_config_to_fdm(fdm):
    """
    Function which initiates deployment of the configuration on given FDM device.
    """
    fdm_deploy_functions.deployfdm(fdm)


if __name__ == '__main__':
    main()



# ASA-FTD object parser
# main.py - Main program
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

from Services import asa_networkobject_functions, asa_networkservice_functions
from Services import fdm_networkobject_functions, fdm_deploy_functions, fdm_serviceobject_functions
from Classes import Devices, Migration
import authorize
import config
import json


def main():
    """
    Main function which initialized one ASA and one FDM object, from the credentials entered in the config.py file.
    Then parse all objects on the ASA to the FDM.
    """

    fdm1 = initialize_fdm()
    asa1 = initialize_asa()

    migration1 = Migration.MigrationStatus()
    parse_objects(asa1, fdm1, migration1)


def parse_objects(asa, fdm, mig):
    """
    Function which first get all objects from ASA as a list, then creates them on the FDM.
    Then gets all object-groups from ASA as a list, then creates them on the FDM.
    An object-group cannot contain a object which does not exist.
    :param asa: Source ASA
    :param fdm: Destination FDM
    :param mig: Migration status
    :return: Nothing
    """

    mig.network_objects_in_asa = asa_networkobject_functions.get_number_of_asa_network_objects(asa)
    mig.network_object_groups_in_asa = asa_networkobject_functions.get_number_of_asa_network_groups(asa)
    mig.service_objects_in_asa = asa_networkservice_functions.get_number_of_asa_service_objects(asa)
    mig.service_object_groups_in_asa = asa_networkservice_functions.get_number_of_asa_service_groups(asa)

    print("Found " + str(mig.network_objects_in_asa) + " network objects on the ASA")
    print("Found " + str(mig.network_object_groups_in_asa) + " network objects on the ASA")
    print("Found " + str(mig.service_objects_in_asa) + " service objects on the ASA")
    print("Found " + str(mig.service_object_groups_in_asa) + " service object-groups on the ASA")

    print("Gathering network objets from ASA: " + asa.ip)
    asa_network_objects = asa_networkobject_functions.get_all_asa_network_objects(asa)
    print("Gathering network object-groups from ASA: " + asa.ip)
    asa_net_groups = asa_networkobject_functions.get_all_asa_network_groups(asa)
    print("Creating network objects on FTD:" + fdm.ip)
    for asa_object in asa_network_objects:
        fdm_networkobject_functions.create_fdm_network_object(fdm, asa_object, mig)
        print("Migrated " + str(mig.migrated_network_objects) + " network objects.")
    print("Network objects created.")

    print("Creating network object-groups on FTD:" + fdm.ip)
    for group in asa_net_groups:
        fdm_networkobject_functions.create_fdm_network_group(fdm, group, mig)
        print("Migrated " + str(mig.migrated_network_object_groups) + " object groups.")
    print("Network object-groups created.")

    print("Gathering service objects from ASA: " + asa.ip)
    asa_service_objects = asa_networkservice_functions.get_all_service_objects(asa)
    print("Creating service objects on FTD:" + fdm.ip)
    for service_object in asa_service_objects:
        fdm_serviceobject_functions.create_fdm_port_object(fdm, service_object, mig)
        print("Migrated " + str(mig.migrated_service_objects) + " services.")
    print("Service objects created.")

    print("Gathering service groups from ASA: " + asa.ip)
    asa_service_groups = asa_networkservice_functions.get_all_service_groups(asa)
    print("Creating service object-groups on FTD:" + fdm.ip)
    for service_group in asa_service_groups:
        fdm_serviceobject_functions.create_fdm_port_group(fdm, asa, service_group, mig)
        print("Migrated " + str(mig.migrated_service_object_groups) + " service groups.")
    print("Service groups created.")

    print("####### Status #######")
    print("Migrated " + str(mig.migrated_network_objects) + " network objects")
    print("Migrated " + str(mig.migrated_network_object_groups) + " network objects")
    print("Migrated " + str(mig.migrated_service_objects) + " service objects")
    print("Skipped " + str(mig.skipped_objects_in_migration()) + " objects")
    print("### Skipped objects ###")
    print(json.dumps(mig.skipped_objects, indent=2, default=str).replace('\\', ''))


def initialize_fdm():
    """
    Initialize an FDM object from info entered in config.py
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
    print("Deployment ID: " + fdm_deploy_functions.deployfdm(fdm)['id'])


def delete_all_objects(fdm):
    """
    Function which first deletes network object-groups, then network objects.
    :param fdm: FDM object
    :return: None
    """
    fdm_networkobject_functions.delete_all_fdm_object_groups(fdm)
    fdm_networkobject_functions.delete_all_fdm_objects(fdm)


if __name__ == '__main__':
    main()

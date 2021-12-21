# ASA-FTD object parser
# main.py - Main program
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

from Services import fdm_networkobject_functions, asa_networkobject_functions, fdm_deploy_functions
from Classes import Devices, Migration
import authorize
import config


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
    :param asa: Soruce ASA
    :param fdm: Destination FDM
    :param mig: Migration status
    :return: Nothing
    """

    mig.network_objects_in_asa = asa_networkobject_functions.get_number_of_asa_network_objects(asa)
    mig.group_objects_in_asa = asa_networkobject_functions.get_number_of_asa_network_groups(asa)

    print("Found " + str(mig.network_objects_in_asa) + " network objects on the ASA")
    print("Found " + str(mig.group_objects_in_asa) + " network objects on the ASA")

    print("Gathering network objets from ASA: " + asa.ip)
    asa_objects = asa_networkobject_functions.get_all_asa_network_objects(asa)

    for asa_object in asa_objects:
        fdm_networkobject_functions.create_fdm_network_object(fdm, asa_object, mig)
        print("Migrated " + str(mig.migrated_network_objects) + " network objects.")

    print("Gathering network objet-groups from ASA: " + asa.ip)
    asa_net_groups = asa_networkobject_functions.get_all_asa_network_groups(asa)
    for group in asa_net_groups:
        fdm_networkobject_functions.create_fdm_network_group(fdm, group, mig)
        print("Migrated " + str(mig.migrated_group_objects) + " object groups.")

    print("####### Status #######")
    print("Migrated " + str(mig.migrated_network_objects) + " network objects")
    print("Migrated " + str(mig.migrated_group_objects) + " network objects")
    print("Skipped " + str(mig.skipped_caused_by_duplicates) + " objects")
    print("### Skipped objects ###")
    for skipped_object in mig.skipped_objects:
        print(skipped_object)


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

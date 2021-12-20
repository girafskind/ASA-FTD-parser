# ASA-FTD object parser
# main.py - Main program
# Version 0.1
# By Bo V Mortensen

import authorize
import config
import classes
import net_objects
import netgroup_objects
import fdmdeploy

def main():

    fdm1 = initfdm()
    asa1 = initasa()

    parseobjects(asa1, fdm1)


def parseobjects(asa, fdm):
    asa_objects = net_objects.getallasanetworkobjects(asa)
    for asa_object in asa_objects:
        net_objects.createfdmnetworkobject(fdm, asa_object)

    asanetgroups = netgroup_objects.getallasanetworkgroups(asa)
    for group in asanetgroups:
        netgroup_objects.createfdmnetworkgroup(fdm, group)


def initfdm():
    newfdm = classes.FTDClass()
    newfdm.ip = config.ftdip
    newfdm.username = config.ftdusername
    newfdm.password = config.ftdpassword
    authorize.fdmgettoken(newfdm)

    return newfdm


def initasa():
    newasa = classes.ASAClass()
    newasa.ip = config.asaip
    newasa.username = config.asausername
    newasa.password = config.asapassword
    newasa.port = config.asaport
    newasa.token = authorize.asagettoken(newasa)

    return newasa


def testfdmdeploy(fdm):
    fdmdeploy.deployfdm(fdm)


if __name__ == '__main__':
    main()



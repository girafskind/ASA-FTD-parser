# ASA-FTD object parser
# main.py - Main program
# Version 0.1
# By Bo V Mortensen

import authorize
import config
import classes
import net_objects
import netgroup_objects

def main():
    #testfdm()
    testasa()
    #hawkasa01 = classes.ASAClass()
    #hawkasa01.ip = config.asaip
    #hawkasa01.username = config.asausername
    #hawkasa01.password = config.asapassword
    #hawkasa01.port = config.asaport
    #hawkasa01.token = authorize.asagettoken(hawkasa01)

    #asaobj = net_objects.getallasanetworkobjects(hawkasa01)
    #for object in asaobj:
    #    print(object)
#    asaobj = netgroup_objects.getallasanetworkgroups(hawkasa01)
#    for object in asaobj:
#        print("Group name")
#        print(object['name'])
#        print("Group members")
#        for member in object['members']:
#            print(member.get('objectId'))

#    objects.getasanetworkobjects(hawkasa01)
#    hawkfp01 = classes.FTDClass()
#    hawkfp01.ip = config.ftdip
#    hawkfp01.username = config.ftdusername
#    hawkfp01.password = config.ftdpassword

#    authorize.fdmgettoken(hawkfp01)

#    print(hawkfp01.expires)
#    print(hawkfp01.refresh_expires)
def testasa():
    hawkasa01 = classes.ASAClass()
    hawkasa01.ip = config.asaip
    hawkasa01.username = config.asausername
    hawkasa01.password = config.asapassword
    hawkasa01.port = config.asaport
    hawkasa01.token = authorize.asagettoken(hawkasa01)

    asaobj = net_objects.getallasanetworkobjects(hawkasa01)
    print(asaobj[0])
    print(asaobj[0]['name'])
    print(asaobj[0]['host']['kind'])
    print(asaobj[0]['host']['value'])

    #testfdm(asaobj[0])
    for object in asaobj:
        testfdm(object)

def testfdm(object):
    hawkfp01 = classes.FTDClass()
    hawkfp01.ip = config.ftdip
    hawkfp01.username = config.ftdusername
    hawkfp01.password = config.ftdpassword

    authorize.fdmgettoken(hawkfp01)

    print(hawkfp01.expires)
    print(hawkfp01.refresh_expires)
    net_objects.createfdmnetworkobject(hawkfp01,object)

if __name__ == '__main__':
    main()



# ASA-FTD-object-parser
Python script for parsing network objects and network object-groups from Cisco ASA to Cisco FDM

The script reads all network objects and object-groups from a Cisco Adaptive Security Appliance (ASA), and then parse the objects and groups to a Cisco Firepower Threat Defence, running the local Firepower Device Manager.

Copy "config-template.py" to "config.py", enter IP-address, username and passwords for FDM and ASA and run main.py

    asaip = "<IP-address of ASA>"
    asausername = "<Username for HTTP access on ASA>"
    asapassword = "<Passowrd for HTTP access on ASA>"
    asaport = "<Port listening on the HTTP service>" (if omitted, it defaults to tcp/443)

    ftdip = "<IP-address of FDM>"
    ftdusername = "<Username for HTTP access on FDM>"
    ftdpassword = "<Passowrd for HTTP access on FDM>"


'main.py' does not take any arguments, simply run:

    python main.py

The script does not deploy the new configration the FDM device, either done manually in the FDM WebUI, or call the "deploy_config_to_fdm" function with the FDM object as argument. 

NB: Current version does not notify if the migration is completed sucessfully.

Written in Python 3.9

Regards girafskind

# ASA-FTD object parser
# Devices.py - class file
# Version 1.0
# By Bo V Mortensen
# 20th December 2021

# ASA device class
class ASAClass:
    username = ""
    password = ""
    ip = ""
    token = ""
    port = "443"

    def url(self):
        url = "https://" + self.ip + ":" + self.port
        return url


# FTD device class
class FTDClass:
    username = ""
    password = ""
    ip = ""
    access_token = ""
    refresh_token = ""
    expires = ""
    refresh_expires = ""
    port = "443"

    def url(self):
        url = "https://" + self.ip + ":" + self.port
        return url
#####################################
#  Broadsign - Register a player    #
#####################################

import os
import requests
import json
import sys
import winreg
from json import dumps
from getmac import get_mac_address as gma
from shutil import copyfile


# API authentication

bs_url = "https://api.broadsign.com:10889/rest/client_registration/v7/add"
bs_token = "<Your token here>"
bs_domain_id = <Your domain ID here (int)>
bs_container_id = <Folder of the future player (int)>
bs_configuration_id = <ID of the configuration profile (int)>

head = {'accept': 'application/json', 'Authorization': 'Bearer {}'.format(bs_token), 'content-type': 'application/json'}

# Creating the datas dict

datas = {
            'container_id' : bs_container_id,
            'domain_id' : bs_domain_id,
            'primary_mac_address' : gma(),
            'target_container_id' : bs_container_id,
            'target_resource_type' : 'host',
            'target_config_profile_bag_id' : bs_configuration_id
            
        }

# Présentation du programme

print("######################################")
print("#  Broadsign - Player registration   #")
print("######################################")

print("\n\n")
        
# Informations nouveau player

datas['hostname'] = input("Enter a player hostname: ")
datas['name'] = datas['hostname']
datas['target_display_unit_id'] = input("Enter display unit ID: ")
datas['primary_mac_address'] = gma()

# Copying BS Player shortcuts to Windows Startup and renaming the player hostname

src = r"C:\programdata\Microsoft\Windows\Start Menu\Programs\Broadsign\BroadSign Player\Broadsign Control Player.lnk"
desktop = r"{}\Desktop\Broadsign Control Player.lnk".format(os.environ['userprofile'])
startup = r"{}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\Broadsign Control Player.lnk".format(os.environ['userprofile'])

print("Renaming player hostname...\n")
try:

    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\services\Tcpip\Parameters', 0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, 'Hostname', 1, winreg.REG_SZ, datas['hostname'])
    winreg.SetValueEx(key, 'NV Hostname', 1, winreg.REG_SZ, datas['hostname'])

except:

    print("Error when renaming the player.")
    sys.exit(1)

print("Copying Broadsign Player shortcut on Windows desktop...")
print("Copying Broadsign Player shortcut on Windows startup...\n")
try:

    copyfile(src, desktop)
    copyfile(src, startup)
    
except:

    print("Error when copying shortcuts.\n")
    sys.exit(1)

# Sending datas on Broadsign API

r = requests.post(bs_url, headers=head, json=datas)

# Checking for errors

if r.status_code != 200:

    print("Error code: {}   Reason: {}".format(r.status_code, r.reason))
    
else:

    r = r.json()
    print("\The player has been successfully registered. To complete the activation process, the player must connect to the BroadSign server. Once this step has been completed, the player will be activated and will be accessible in the Player or Edge Server section of Broadsign Control: {}\n".format(r['client_registration'][0]['id']))
    
    os.system("pause")

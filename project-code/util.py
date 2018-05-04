'''
author: Shagufta Pathan
purpose: util code that reads config file and exposes those settings via getters
'''

import yaml
import sys
import logging
from os.path import expanduser

HOME = expanduser("~")
CREDFILE = HOME+"/.cloudmesh/class.yaml"

try:
    cred = yaml.load(open(CREDFILE))
    if cred['clouds']['tacc']['name'] == 'Chameleon TACC':
        auth_username = cred['clouds']['tacc']['credentials']['OS_USERNAME']
        auth_password = cred['clouds']['tacc']['credentials']['OS_PASSWORD']
        auth_url = cred['clouds']['tacc']['credentials']['OS_AUTH_URL']
        project_name = cred['clouds']['tacc']['credentials']['OS_PROJECT_NAME']
        region_name = cred['clouds']['tacc']['credentials']['OS_REGION_NAME']

        os_default_flavor = cred['clouds']['tacc']['default']['flavor']
        os_default_image = cred['clouds']['tacc']['default']['image']
        os_default_secgroup = cred['clouds']['tacc']['default']['secgroup']
        os_default_keypair = cred['clouds']['tacc']['default']['keypairname']

        if auth_username == "TBD" or auth_password =="TBD":
            logging.error('Please save openstack Chameleon cloud credentials in class.yaml')
            sys.exit(1)

except OSError:
    logging.error('Please create class.yaml with credential info')
    sys.exit(1) 

# cloud-init config variable
# Enter the commands you would like to execute on the instance created

userdata = '''#!/bin/bash
echo "System Information: $(uname -a)" | tee /home/cc/output.txt
echo "The time is now $(date -R)!" | tee -a /home/cc/output.txt
echo "The hostname is $(hostname)" | tee -a /home/cc/output.txt
echo "ifconfig details: $(ifconfig)" | tee -a /home/cc/output.txt
'''

def getOSAuthUsername():
    return auth_username

def getOSAuthPassword():
    return auth_password

def getOSAuthURL():
    return auth_url

def getOSProjectName():
    return project_name

def getOSRegionName():
    return region_name

def getOSDefaultFlavor():
    return os_default_flavor

def getOSDefaultImage():
    return os_default_image

def getOSDefaultSecGroup():
    return os_default_secgroup

def getOSDefaultKeypairName():
    return os_default_keypair

def getOSUserData():
    return userdata



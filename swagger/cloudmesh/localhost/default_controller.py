# I referred the below websites for the Basic Authentication code part:
# http://flask.pocoo.org/snippets/8/
# https://github.com/zalando/connexion/blob/master/examples/basicauth/app.py

import connexion
import six

from swagger_server.models.entities import ENTITIES  # noqa: E501
from swagger_server import util

import subprocess 
from flask import request
from urlparse import urlparse
import flask
import auth_util 
import json

@auth_util.requires_auth
def localhost_post(entities=None):  # noqa: E501
    """localhost_post

    Executes command on the specified host # noqa: E501

    :param command: The command to execute on the specified host
    :type command: str
    :param entities: The username and hostname to execute the command on
    :type entities: dict | bytes
    :rtype: None
    """
    user = entities['userName']
    host = entities['hostName']
    command = entities['command']
    '''
    splitCom = command.split()
    splitCom.insert(0, 'ssh')
    splitCom.insert(1, '-t')
    splitCom.insert(2, user+'@'+host)
    '''
    if connexion.request.is_json:
        entities = ENTITIES.from_dict(connexion.request.get_json())  # noqa: E501
    base_url = request.url_root
    parse_url = urlparse(base_url)
    if parse_url.netloc == "127.0.0.1:8080" or parse_url.netloc == "localhost:8080":
        #s = subprocess.check_output('ssh '+user+'@'+host+' '+command, shell=True).strip().split('\n')
        s = subprocess.check_output(command).strip().split('\n')
        return s
    else:
        return "Error: Connections only allowed from localhost"

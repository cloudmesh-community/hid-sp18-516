import connexion
import six

from swagger_server.models.entities import ENTITIES  # noqa: E501
from swagger_server import util

import subprocess
from flask import request
from urlparse import urlparse

import connexion
import flask

try:
    from decorator import decorator
except ImportError:
    import sys
    import logging
    logging.error('Missing dependency. Please run `pip install decorator`')
    sys.exit(1)

def check_auth(username, password):
    '''This function is called to check if a username /
    password combination is valid.'''
    return username == 'admin' and password == 'secret'

def authenticate():
    '''Sends a 401 response that enables basic auth'''
    return flask.Response('You have to login with proper credentials', 401,
                          {'WWW-Authenticate': 'Basic realm="Login Required"'})

@decorator
def requires_auth(f, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return f(*args, **kwargs)

@requires_auth
def command_post(command, entities=None):  # noqa: E501
    """command_post

    Executes command on the specified host # noqa: E501

    :param command: The command to execute on the specified host
    :type command: str
    :param entities: The username and hostname to execute the command on
    :type entities: dict | bytes

    :rtype: None
    """
    #print("The command is:", command)
    #print("The entities are:", entities)
    splitCom = command.split()

    if connexion.request.is_json:
        entities = ENTITIES.from_dict(connexion.request.get_json())  # noqa: E501
    base_url = request.url_root
    o = urlparse(base_url)
    if o.netloc == "127.0.0.1:8080" or o.netloc == "localhost:8080":
        s = subprocess.check_output(splitCom)
        output = s.split('\n')
        return output
    else:
        return "Could not execute command on the specified host"

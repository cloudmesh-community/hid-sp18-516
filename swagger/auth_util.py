import yaml
import flask
from os.path import expanduser

HOME = expanduser("~")
CREDFILE = HOME+"/.cloudmesh/security.yaml"
config = yaml.load(open(CREDFILE))

"""
try:
    config = yaml.load(open('~/.cloudmesh/security.yaml'))
except IOError:
      print "Error: File does not appear to exist."
"""
try:
    from decorator import decorator
except ImportError:
    import sys
    import logging
    logging.error('Missing dependency. Please run `pip install decorator`')
    sys.exit(1)

def authenticate():
    '''Sends a 401 response that enables basic auth'''
    return flask.Response('You have to login with proper credentials', 401,
                          {'WWW-Authenticate': 'Basic realm="Login Required"'})

def check_auth(username, password):
    '''This function is called to check if a username /
    password combination is valid.'''
    for key in config:
        if username == config[key]['username'] and password == config[key]['password']:
            return True
        else:
            continue
    return False

@decorator
def requires_auth(f, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return f(*args, **kwargs)


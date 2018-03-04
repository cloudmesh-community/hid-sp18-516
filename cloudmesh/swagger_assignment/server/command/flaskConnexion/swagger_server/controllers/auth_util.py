import yaml

config=yaml.load(open('creds/config.yaml'))

def check_auth(username, password):
    '''This function is called to check if a username /
    password combination is valid.'''
    for key in config:
        if not username == config[key]['username'] and password == config[key]['password']:
            continue
        else:      
            break   
    return True

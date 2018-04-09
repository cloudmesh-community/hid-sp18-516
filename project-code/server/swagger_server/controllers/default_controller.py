import connexion
import six

from swagger_server.models.attributes import ATTRIBUTES  # noqa: E501
from swagger_server.models.delete import DELETE  # noqa: E501
from swagger_server.models.flavor import FLAVOR  # noqa: E501
from swagger_server.models.images import IMAGES  # noqa: E501
from swagger_server.models.instance import INSTANCE  # noqa: E501
from swagger_server.models.keypair import KEYPAIR  # noqa: E501
from swagger_server.models.security import SECURITY  # noqa: E501
from swagger_server import util

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import time

auth_username = '<enter your username here>'
auth_password = '<enter your password here>'
auth_url = 'https://openstack.tacc.chameleoncloud.org:5000'
project_name = 'CH-819337'
region_name = 'RegionOne'

provider = get_driver(Provider.OPENSTACK)
conn = provider(auth_username,
                auth_password,
                ex_force_auth_url=auth_url,
                ex_force_auth_version='2.0_password',
                ex_tenant_name=project_name,
                ex_force_service_region=region_name)

def addkeypair_post(keypair=None):  # noqa: E501
    """addkeypair_post

    Add a SSH KeyPair and associate with the instance # noqa: E501

    :param keypair: Provide the instance name, ssh keypair name and the public key in body
    :type keypair: dict | bytes

    :rtype: None
    """
    instance_name = keypair['instance_name']
    keypair_name = keypair['keypair_name']
    public_key = keypair['public_key']

    if connexion.request.is_json:
        keypair = KEYPAIR.from_dict(connexion.request.get_json())  # noqa: E501
    #return 'do some magic!'
    print('Checking for existing SSH key pair...')
    keypair_exists = False

    for keypair in conn.list_key_pairs():
        if keypair.name == keypair_name:
            keypair_exists = True
            break

    if keypair_exists:
        return('Keypair ' + keypair_name + ' already exists. Skipping import.')
    else:
        print('adding keypair...')
        conn.import_key_pair_from_file(keypair_name, pub_key_file)
        return('Keypair was added successfully!')

def create_instance_post(attributes=None):  # noqa: E501
    """create_instance_post

    Create an instance # noqa: E501

    :param attributes: The name,imagename/id, flavor id, ssh keypair name, ssh public key to create an instance as payload
    :type attributes: dict | bytes

    :rtype: None
    """
    instance_name = attributes['instance name']
    image_id = attributes['image id/name']
    flavor_id = attributes['flavor id']
    keypair_name = attributes['keypair name']
    security_group_name = attributes['security group']
     
    image = conn.get_image(image_id)
    flavor = conn.ex_get_size(flavor_id)
    
    for security_group in conn.ex_list_security_groups():
        if security_group.name == security_group_name:
            all_in_one_security_group = security_group
    
    #print(instance_name, image_id, flavor_id, keypair_name, all_in_one_security_group)
    
    if connexion.request.is_json:
        attributes = ATTRIBUTES.from_dict(connexion.request.get_json())  # noqa: E501
        #return 'do some magic!'
        
    print('Checking for existing instance...')
    instance_exists = False
    for instance in conn.list_nodes():
        if instance.name == instance_name:
            testing_instance = instance
            instance_exists = True
            break

    if instance_exists:
        return('Instance ' + testing_instance.name + ' already exists. Skipping creation.')
    else:
        testing_instance = conn.create_node(name=instance_name, image=image, size=flavor, ex_keyname=keypair_name, ex_security_groups=[all_in_one_security_group])

        #testing_instance = conn.create_node(name=instance_name, image=image, size=flavor)
        return 'Instance was created successfully'    

def delete_instance_instance_name_delete(instance_name):  # noqa: E501
    """delete_instance_instance_name_delete

    Delete an instance # noqa: E501

    :param instance_name: Provide the instance name in path
    :type instance_name: str

    :rtype: DELETE
    """
    #return 'do some magic!'
    print('Checking for existing instance...')
    print(instance_name)
    #instance_name = instnace
    instance_exists = False
    for instance in conn.list_nodes():
        if instance.name == instance_name:
            testing_instance = instance
            instance_exists = True
            conn.destroy_node(testing_instance)
            return 'Instance was deleted successfully'
       
    return 'Instance was not found, exiting!'

def flavor_get():  # noqa: E501
    """flavor_get

    Returns a list of flavors available # noqa: E501


    :rtype: FLAVOR
    """
    #return 'do some magic!'
    flvr_list = []
    flavors = conn.list_sizes()
    for flavor in flavors:
        node = {}
        node["id"] = flavor.id
        node["name"] = flavor.name
        node["ram"] = flavor.ram
        node["disk"] = flavor.disk
        node["bandwidth"] = flavor.bandwidth
        node["vcpus"] = flavor.vcpus
        flvr_list.append(node)
    return flvr_list

def floating_ippost(instance_name=None):  # noqa: E501
    """floating_ippost

    Attach a floating IP with the instance # noqa: E501

    :param instance_name: Provide the instance name to attach the floating IP in body
    :type instance_name: dict | bytes

    :rtype: None
    """
    inst_name = instance_name['instance_name']
    print(instance_name)
    if connexion.request.is_json:
        instance_name = DELETE.from_dict(connexion.request.get_json())  # noqa: E501
    #return 'do some magic!'
    print('Checking for existing instance...')
    instance_exists = False
    for instance in conn.list_nodes():
        print(instance.name)
        print(instance_name)
        if instance.name == inst_name:
            testing_instance = instance
            instance_exists = True
            break
        else:
            return 'Instance does not exist, exiting!'
    
    print('Checking for unused Floating IP...')
    unused_floating_ip = None
    for floating_ip in conn.ex_list_floating_ips():
        if not floating_ip.node_id:
            unused_floating_ip = floating_ip
            print(unused_floating_ip)
            break

    if not unused_floating_ip and len(conn.ex_list_floating_ip_pools()):
        pool = conn.ex_list_floating_ip_pools()[0]
        print('Allocating new Floating IP from pool: {}'.format(pool))
        unused_floating_ip = pool.create_floating_ip()

#To determine whether a public IP address is assigned to your instance:
    public_ip = None
    if len(testing_instance.public_ips):
        public_ip = testing_instance.public_ips[0]
        print('Public IP found: {}'.format(public_ip))


#Attach the floating IP address to the instance:
    if public_ip:
        return 'Instance ' + testing_instance.name + ' already has a public ip. Skipping attachment.'
    elif unused_floating_ip:
        conn.ex_attach_floating_ip_to_node(testing_instance, unused_floating_ip)
        return 'Floating IP was attached successfully!'

def images_get():  # noqa: E501
    """images_get

    Returns a list of images available # noqa: E501


    :rtype: IMAGES
    """
    #return 'do some magic!'

    img_list = []
    images = conn.list_images()
    for image in images:
        node = {}
        node["id"] = image.id
        node["name"] = image.name
        node["status"] = image.extra['status']
        img_list.append(node)
    return img_list

def list_instances_get():  # noqa: E501
    """list_instances_get

    Returns a list of instances available # noqa: E501


    :rtype: INSTANCE
    """
    #return 'do some magic!'
    inst_list = []
    instances = conn.list_nodes()
    for instance in instances:
        node = {}
        node["uuid"] = instance.uuid
        node["name"] = instance.name
        node["state"] = instance.state
        node["public_ips"] = instance.public_ips
        node["private_ips"] = instance.private_ips
        node["imageId"] = instance.extra['imageId']
        node["created"] = instance.extra['created']
        node["flavorId"] = instance.extra['flavorId']
        node["tenantId"] = instance.extra['tenantId']
        node["key_name"] = instance.extra['key_name']
        inst_list.append(node)
    return inst_list
 
def securitygroup_post(security=None):  # noqa: E501
    """securitygroup_post

    Create security group if not already existing # noqa: E501

    :param security: Provide the instance name and the security group name in body
    :type security: dict | bytes

    :rtype: None
    """
    security_group_name = security['group_name']
    if connexion.request.is_json:
        security = SECURITY.from_dict(connexion.request.get_json())  # noqa: E501
    #return 'do some magic!'
    security_group_exists = False
    for security_group in conn.ex_list_security_groups():
        if security_group.name == security_group_name:
            all_in_one_security_group = security_group
            security_group_exists = True
            break

    if security_group_exists:
        return ('Security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
    else:
        all_in_one_security_group = conn.ex_create_security_group(security_group_name, 'network access for all-in-one application.')
        conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 80, 80)
        conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 22, 22)

    for security_group in conn.ex_list_security_groups():
        print(security_group)

def start_instance_post(instance_name=None):  # noqa: E501
    """start_instance_post

    Start a stopped instance # noqa: E501

    :param instance_name: Provide the instance name in the body
    :type instance_name: dict | bytes

    :rtype: None
    """
    inst_name = instance_name['instance_name']
    if connexion.request.is_json:
        instance_name = DELETE.from_dict(connexion.request.get_json())  # noqa: E501
    #return 'do some magic!'
    for instance in conn.list_nodes():
        if instance.name == inst_name and instance.state == 'stopped':
            conn.ex_start_node(instance) 
            time.sleep(15)
            print(instance.state)
            return('Instance has been started')
 
def stop_instance_post(instance_name=None):  # noqa: E501
    """stop_instance_post

    Stop an instance # noqa: E501

    :param instance_name: Provide the instance name in the body
    :type instance_name: dict | bytes

    :rtype: None
    """
    inst_name = instance_name['instance_name']
    if connexion.request.is_json:
        instance_name = DELETE.from_dict(connexion.request.get_json())  # noqa: E501
    #return 'do some magic!'
    for instance in conn.list_nodes():
        if instance.name == inst_name and instance.state == 'running':
            conn.ex_stop_node(instance)
            time.sleep(15)
            print(instance.state)
            return('Instance has been stopped')


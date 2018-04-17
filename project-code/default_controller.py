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
import yaml
import util
import sys
import logging

auth_username = util.getOSAuthUsername()
auth_password = util.getOSAuthPassword()
auth_url = util.getOSAuthURL()
project_name = util.getOSProjectName()
region_name = util.getOSRegionName()
os_default_flavor = util.getOSDefaultFlavor()
os_default_image = util.getOSDefaultImage()
os_default_secgroup = util.getOSDefaultSecGroup()
os_default_keypair = util.getOSDefaultKeypairName()

provider = get_driver(Provider.OPENSTACK)
conn = provider(auth_username,
                auth_password,
                ex_force_auth_url=auth_url,
                ex_force_auth_version='2.0_password',
                ex_tenant_name=project_name,
                ex_force_service_region=region_name)

def addfloating_ip(param=None):  # noqa: E501
    """addfloating_ip

    Attach a floating IP with the instance # noqa: E501

    :param param: Provide the instance name to attach the floating IP in body
    :type param: dict | bytes

    :rtype: None
    """
    inst_name = param['instance_name']
    print(inst_name)

    if connexion.request.is_json:
        param = DELETE.from_dict(connexion.request.get_json())  # noqa: E501
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

def addkeypair(params=None):  # noqa: E501
    """addkeypair

    Add a new SSH KeyPair on the cloud # noqa: E501

    :param params: Provide the ssh keypair name and the public key as payload
    :type params: dict | bytes

    :rtype: None
    """
    keypair_name = params['keypair_name']
    public_key = params['public_key']

    if connexion.request.is_json:
        params = KEYPAIR.from_dict(connexion.request.get_json())  # noqa: E501

    print('Checking for existing SSH key pair...')
    keypair_exists = False

    for keypair in conn.list_key_pairs():
        if keypair.name == keypair_name:
            keypair_exists = True
            break

    if keypair_exists:
        return('Keypair ' + keypair_name + ' already exists. Skipping import.')
    else:
        print('Adding keypair...')
        conn.import_key_pair_from_file(keypair_name, pub_key_file)
        return('Keypair was added successfully!')

def addsecuritygroup(param=None):  # noqa: E501
    """addsecuritygroup

    Create security group if not already existing # noqa: E501

    :param param: Provide the security group name in body
    :type param: dict | bytes

    :rtype: None
    """
    security_group_name = param['group_name']

    if connexion.request.is_json:
        param = SECURITY.from_dict(connexion.request.get_json())  # noqa: E501
    security_group_exists = False
    for security_group in conn.ex_list_security_groups():
        if security_group.name == security_group_name:
            all_in_one_security_group = security_group
            security_group_exists = True
            break

    if security_group_exists:
        return ('Security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
    else:
        all_in_one_security_group = conn.ex_create_security_group(security_group_name, 'Security Group')
        conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 80, 80)
        conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 22, 22)
        for security_group in conn.ex_list_security_groups():
            if security_group.name == security_group_name:
                return('Security group ' + security_group.name + ' was created successfully')

def create_vm(attributes=None):  # noqa: E501
    """create_vm

    Create an instance # noqa: E501

    :param attributes: Provide the instance name(required),image name/id, flavor id, ssh keypair name, security group to create an instance as payload
    :type attributes: dict | bytes

    :rtype: None
    """
    img_id = None
    flvr_id = None
    keypair_nm = None
    security_group_name = None
    instance_name = attributes['instance_name']

    if 'image_id' in attributes.keys():
        img_id = attributes['image_id']

    if not img_id:
        images = conn.list_images()
        for img in images:
            if img.name == os_default_image:
                image = img
    else:
        image = conn.get_image(img_id)

    if 'flavor_id' in attributes.keys():
        flvr_id = attributes['flavor_id']
    if not flvr_id:
       flavors = conn.list_sizes()
       for flavr in flavors:
           if flavr.name == os_default_flavor:
               flavor = flavr
    else:
        flavor = conn.ex_get_size(flvr_id)
    if 'security_group' in attributes.keys():
        security_group_name = attributes['security_group']
    if not security_group_name:
        security_group_name = os_default_secgroup
        for security_group in conn.ex_list_security_groups():
            if security_group.name == security_group_name:
                all_in_one_security_group = security_group

    else:
        for security_group in conn.ex_list_security_groups():
            if security_group.name == security_group_name:
                all_in_one_security_group = security_group

    if 'keypair_name' in attributes.keys():
        keypair_name = attributes['keypair_name']
    if not keypair_nm:
        keypair_name = os_default_keypair

    if connexion.request.is_json:
        attributes = ATTRIBUTES.from_dict(connexion.request.get_json())  # noqa: E501

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

def delete_vm(instance_name):  # noqa: E501
    """delete_vm

    Delete an instance # noqa: E501

    :param instance_name: Provide the instance name in path
    :type instance_name: str

    :rtype: DELETE
    """
    print('Checking for existing instance...')
    print(instance_name)
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

def images_get():  # noqa: E501
    """images_get

    Returns a list of images available # noqa: E501


    :rtype: IMAGES
    """
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

def start_vm(param=None):  # noqa: E501
    """start_vm

    Start a stopped instance # noqa: E501

    :param param: Provide the instance name in the body
    :type param: dict | bytes

    :rtype: None
    """
    if 'instance_name' not in param.keys():
        return('Please provide the instance name in json format')
    else:
        inst_name = param['instance_name']
        print('Checking for existing instance...')

    if connexion.request.is_json:
        param = DELETE.from_dict(connexion.request.get_json())  # noqa: E501

        instance_exists = False
        for instance in conn.list_nodes():
            if instance.name == inst_name:
                #testing_instance = instance
                instance_exists = True
                print('Instance exists')
                if instance.state == 'stopped':
                    conn.ex_start_node(instance)
                    return('Instance has been started successfully')
                elif instance.state == 'running':
                    return('Instance is already running, exiting!')
                else:
                    return('Instance is not in stopped state', instance.state)

    return('Instance does not exist, exiting!')

def stop_vm(param=None):  # noqa: E501
    """stop_vm

    Stop an instance # noqa: E501

    :param param: Provide the instance name in the body
    :type param: dict | bytes

    :rtype: None
    """
    if 'instance_name' not in param.keys():
        return('Please provide the instance name in json format')
    else:
        inst_name = param['instance_name']
        print('Checking for existing instance...')

    if connexion.request.is_json:
        param = DELETE.from_dict(connexion.request.get_json())  # noqa: E501
        instance_exists = False
        for instance in conn.list_nodes():
            if instance.name == inst_name:
                #testing_instance = instance
                instance_exists = True
                print('Instance exists')
                if instance.state == 'running':
                    conn.ex_stop_node(instance)
                    return('Instance has been stopped successfully')
                elif instance.state == 'stopped':
                    return('Instance has been already stopped, exiting!')
                else:
                    return('Instance is not in running state', instance.state)

    return('Instance does not exist, exiting!')

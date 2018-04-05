from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

auth_username = 'spathan'
auth_password = '123Chameleon!@#'
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
'''
images = conn.list_images()
for image in images:
    print(image)

flavors = conn.list_sizes()
for flavor in flavors:
    print(flavor)
'''
image_id = '1895dc93-7cd8-4b46-a252-4eb55b80859f'
image = conn.get_image(image_id)
print(image)

flavor_id = '2'
flavor = conn.ex_get_size(flavor_id)
print(flavor)

'''
instance_name = 'testing'
testing_instance = conn.create_node(name=instance_name, image=image, size=flavor)
print(testing_instance)


conn.destroy_node(testing_instance)

instances = conn.list_nodes()
for instance in instances:
    print(instance)

'''
print('Checking for existing SSH key pair...')
keypair_name = 'openstackVM'
pub_key_file = '~/.ssh/openstackVM.pub'
keypair_exists = False

for keypair in conn.list_key_pairs():
    if keypair.name == keypair_name:
        keypair_exists = True
        break

if keypair_exists:
    print('Keypair ' + keypair_name + ' already exists. Skipping import.')
else:
    print('adding keypair...')
    conn.import_key_pair_from_file(keypair_name, pub_key_file)

for keypair in conn.list_key_pairs():
    print(keypair)


# Creating Security Group

print('Checking for existing security group...')
security_group_name = 'default'
security_group_exists = False
for security_group in conn.ex_list_security_groups():
    if security_group.name == security_group_name:
        all_in_one_security_group = security_group
        security_group_exists = True
        break

if security_group_exists:
    print('Security Group ' + all_in_one_security_group.name + ' already exists. Skipping creation.')
else:
    all_in_one_security_group = conn.ex_create_security_group(security_group_name, 'network access for all-in-one application.')
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 80, 80)
    conn.ex_create_security_group_rule(all_in_one_security_group, 'TCP', 22, 22)

for security_group in conn.ex_list_security_groups():
    print(security_group)


# Boot and configure an instance

print('Checking for existing instance...')
instance_name = 'all-in-one'
instance_exists = False
for instance in conn.list_nodes():
    if instance.name == instance_name:
        testing_instance = instance
        instance_exists = True
        break

if instance_exists:
    print('Instance ' + testing_instance.name + ' already exists. Skipping creation.')
else:
    testing_instance = conn.create_node(name=instance_name,
                                        image=image,
                                        size=flavor,
                                        ex_keyname=keypair_name,
                                        ex_security_groups=[all_in_one_security_group])
    conn.wait_until_running([testing_instance])

for instance in conn.list_nodes():
    print(instance)

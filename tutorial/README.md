# OpenStack Cluster Setup 

## Overview
OpenStack is an Infrastructure as a Service platform that allows to create and manage virtual environments. It is a free and opensource software for cloud computing, that controls large pools of compute, storage and networking resources throughout a datacenter managing it either via dashboard or through the OpenStack API. The OpenStack software can be easily accessed via the OpenStack Web Interface called `Horizon` provided by Chameleon. Chameleon provides an installation of OpenStack version 2015.1 (Kilo) using the KVM virtualization technology. 

In this tutorial, we are going to create some instances using Horizon and create a cluster from those instances. For the purpose  of this tutorial, we will create just 3 instances to show how a cluster can be set-up. We will name the instances as `<username-hidNumber>-01`, `<username-hidNumber>-02` and `<username-hidNumber>-03`. 

The first step is to create the Instances. For this you need to log in to the web interface using Chameleon username and password. 
Make sure you are added to the correct project. There are couple of things that needs to be done to set up an instance. I will cover it breifly here, you can refer to either Chameleon Cloud chapter in the handbook or visit the Chameleon page <https://www.chameleoncloud.org/docs/user-guides/openstack-kvm-user-guide/> for more details. To create an instance:
  * Go to the Instances page by clicking on the left menu. Click on `Launch Instance` button, leave the Availability Zone to `nova`, enter the `instance name`, choose the flavor (small for this tutorial). Choose the Instance Boot Source as `Boot from Image` and choose the Image name as `CC-Ubuntu16.04`. 
  * In order to access the instance from your own VM, you need to add the SSH Keypair for the instance. You can do this by clicking on the `Access & Security` tab. Enter a name for the key and paste your VM's public key in the textbox provided. Choose the `Security groups` as default. 
  * In the Networking tab, you select the network to be associated with your instance. Hence make sure your project's private name is added, not the ext-net. You can do this using the `+` and `-` buttons.
  * Click on the Launch button at the bottom of the form.

The second step is to assign floating IPs to the instances. By default, instances are automatically assigned a private IP address. Floating IPs assign public IP address to the instance. Public addresses are used for communication with networks outside the cloud, including the Internet. This can be done while the Instance is booting up. Click on the dropdown under `Actions` and choose `Associate Floating IP`. Choose an IP from the IP Address menu and click Associate. If there are no addresses available, click the `+` and follow the prompts to add one. Create all 3 instances one by one in the same way. 

The next step to generate passwordless keys on all the 3 instances. To do this:
  * Open a terminal and ssh to the instance from your VM using the command:
  `ssh cc@<floatingIPofInstance1>`
  
  This should log you in automatically in to your instance.
  * Generate passwordless ssh keys using the command:
  `ssh keygen -t rsa`
 
 Enter filename in which to save the keys. I entered as `/home/cc/.ssh/id_rsa_01` since I already have a key id_rsa. 
 Press `enter` when it prompts for passphrase.
 You should have 2 keys generated. A private key(id_rsa_01) and a public key (id_rsa_01.pub).

 Repeat the same steps for instances 2 and 3.

The next step is to copy the public keys on one instance into the authorized_keys file of the other instances.
  * For this, open 3 terminals. run the commands from your own VM:
  
  `ssh cc@<floatingIPofInstance1>`
  
  `ssh cc@<floatingIPofInstance2>`
  
  `ssh cc@<floatingIPofInstance3>`

  * Open the public key file contents of instance1(id_rsa_01.pub) using cat command:
  
  `cat ~/.ssh/id_rsa_01.pub`

    Copy the contents and paste it into the ~/.ssh/authorized_keys file of instance2 and instance3.

  * Then, open the public key file contents of instance2(id_rsa_02.pub) using cat command:
  
  `cat ~/.ssh/id_rsa_02.pub`

    Copy the contents and paste it into the ~/.ssh/authorized_keys file of instance1 and instance3.

  * Next, open the public key file contents of instance3(id_rsa_02.pub) using cat command:
  
  `cat ~/.ssh/id_rsa_03.pub`
    
    Copy the contents and paste it into the ~/.ssh/authorized_keys file of instance1 and instance2.

Once this is done, the authorized_keys file on one instance should have the public keys of all the other instances, including the public key of your own VM (since you had added that earlier while creating the instance).

Now, you should be able to ssh between these instances using either floatingIP or the PrivateIP. But be sure to provide the private key of the instance that you are logging in from. Run the following commands to verify:
  * First login to one of instance1 using `ssh cc@<floatingIPofInstance1>` from your own VM.
  * Now ssh to another instance, either 2 or 3 using `ssh -i <privateKeyofInstance1:id_rsa_01> cc@<floatingIPofInstance2>`
  * The prompt should now change to instance2. 
  * Try to ssh from instance1 to instance3, from instance2 to instance1/instance3 or from instance3 to instance1/instance2. 
  * It should login in successfully to these instances.
  * Instead of providing the private_key, you can avoid that by starting ssh_agent process and then adding the private key using ssh add. To do this run the following commands on all instances with the correct private_key name:
  
  `eval "$(ssh-agent -s)"`
  
  `ssh-add ~/.ssh/id_rsa`
  
Our goal was to set up a cluster using the instances created on Openstack. Now you are able to successfully login to each of these instances and the instances are also able to login to each other. 

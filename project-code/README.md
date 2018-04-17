## Instructions for executing the project using docker

* git clone the project.

* you should have docker installed on your machine.

* change the directory to **project-code** folder.

* Build the docker image including the program using following make command
  
  * ```make docker-build```

* Start the service using following make command
  
  * ```make docker-start```
  
* If you need to start the container in detached mode, you can use following make command.
  
  * ```make docker-start-detach-mode```

* Test the service using the following make commands
  
  * ```make test_VMs```
  
  * ```make test_images```
  
  * ```make test_flavors```
  
  * ```make test_createVM```
  
  * ```make test_secgroup```
  
  * ```make test_keypair```
  
  * ```make test_floatingIP```
  
  * ```make test_stopVM```
  
  * ```make test_startVM```
  
  * ```make test_deleteVM```
  
  

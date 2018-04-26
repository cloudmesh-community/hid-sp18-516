## Prerequisites for Execution

* git clone the repository.

* you should have docker installed on your machine.

* you should have account on Chameleon cloud and keep your credentials handy

* change the directory to **project-code** folder.

* In the **class.yaml**, make sure to update the `OS_USERNAME` and `OS_PASSWORD` with your Chameleon cloud `username` and `password` instead of `TBD` for TACC cloud.

* Make sure to download the **swagger-codegen-cli.jar** file in the `project-code` directory if executing the project without using docker.

* In the **Makefile**, for the `test_keypair` target, update the `keypair name` and the `public keyfile path` with your own keypair name and public keyfile path that you want to add to the cloud as shown in the example in Makefile.

## Instructions for executing the project using docker

* Follow the prerequisites mentioned above

* Build the docker image using the following make command from Makefile
  
  * ```make docker-build```

* Start the service using following make command
  
  * ```make docker-start```
  
* If you need to start the container in detached mode, you can use following make command.
  
  * ```make docker-start-detach-mode```
  
* If you need to stop the docker container, use the following make command.
  
  * ```make docker-stop```

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
  
* After executing each target, you can log onto Chameleon cloud and verify the result.

## Instructions for executing the project without docker

* Follow the prerequisites mentioned above

* To generate the Swagger code and create the Swagger service, execute the make command from the Makefile
  
  * ```make service```
  
* To start the Swagger server, run the command

  * ```make start```
  
* If you need to stop the Swagger server, run the following make command.
  
  * ```make stop```
  
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
 
* After executing each target, you can log onto Chameleon cloud and verify the result.
  

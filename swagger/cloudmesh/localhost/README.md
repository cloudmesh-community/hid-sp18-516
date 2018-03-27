# Swagger Cloud and Big Data Rest Service

## Objective :

This REST API is intended to allow users to request execution of a system `command` on specified `hostname`, along with the 
specified `username`. 
It should use basic authentication.
The REST service should conform to Swagger/OpenAPI 2.0 specification. 

## Implementation :
* The basics of the REST service is defined in the YAML document `localhost.yaml` file
* POST operation has been implemented to post the command, username and hostname
* The server-side code has been generated using Swagger Codegen
* Modules like `subprocess` and `flask` have been used for the actual implementation
* The security credentials are stored in the `security.yaml` file
* Basic Authentication code is stored in `auth_util.py` file
* This servie has been tested with 2 VMs. The second VM was set to passwordless SSH. VM1 does ssh to VM2 and executes the specified command on VM2.

## Execution Details :
* Make sure you have swagger-codegen-cli.jar installed in your working directory
* git clone the swagger directory
* On your terminal, using the Makefile provided run the following commands:
  * `make service`
  * `make start`
  * You should see a message like this:
  ``` 
  Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
  ```
* On another terminal to test the service, run:
    * `make test`
    
* To kill the service, run:
  * `make stop`
  
* To clean the directories, run:
  * `make clean`
  
* To create a docker image and build the image, simple run:
  * `make container`
  
  * To test the service on the docker container, first you need to login to the container using the command:
  
  `sudo docker exec -it <containerID> bash`
  
  * Then execute the following curl command on the shell of the container;
  ```
  curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "<username>", "hostName": "localhost", "command": "ls -l"}' http://localhost:8080/cloudmesh/localhost
  ```
  * To stop the running container, first `exit` the container that you were logged into and simply run the following command:
  
  `sudo docker stop $(sudo docker ps -a -q -f status=running)`
  
## Examples that you can use to test the service, just add them in the `test` target in the Makefile:
```
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "sheena", "hostName": "192.168.56.102", "command": "ls -l"}' http://localhost:8080/cloudmesh/localhost

Output:
[
  "total 44",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Desktop",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Documents",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Downloads",
  "-rw-r--r-- 1 sheena sheena 8980 Mar  6 23:39 examples.desktop",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Music",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Pictures",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Public",
  "-rw-rw-r-- 1 sheena sheena    0 Mar  7 01:27 saifwashere",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Templates",
  "drwxr-xr-x 2 sheena sheena 4096 Mar  7 00:02 Videos"
]
```

```
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "sheena", "hostName": "192.168.56.102", "command": "uname -a"}' http://localhost:8080/cloudmesh/localhost

Output:
[
  "Linux sheena-VirtualBox 4.10.0-28-generic #32~16.04.2-Ubuntu SMP Thu Jul 20 10:19:48 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux"
]
```

* When you do not give the Authorization header, it throws an error saying: `You have to login with proper credentials`
```
curl -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost", "command": "uname -a"}' http://localhost:8080/cloudmesh/localhost
You have to login with proper credentials
```

* If you do not have another VM setup for test, you can test on your own VM as hostname as `localhost` and username as `<your-username>`

## Note :
* Since I am using POST, the execution is done via curl. It takes 3 arguments: `hostname`, `username` and `command`.
* Use the correct base64 encoded string in the header for the authentication.
* If you use `localhost` as hostname for testing, it waits for the authentication on the server-side to execute the command, make sure to enter your password on the server-side.

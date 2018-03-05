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
* The security credentials are stored in the security.yaml file

## Execution Details :
* Make sure you have swagger-codegen-cli.jar installed in your working directory
* git clone the swagger directory
* On your terminal, using the Makefile provided run the following commands:
  * `make service`
  * `make run`
  * You should see a message like this:
  ``` 
  Running on http://0.0.0.0:8080/ (Press CTRL+C to quit)
  ```
* On another terminal to test the service, run:
    * `make test`
    
* To kill the service, run:
  * `make stop`
  
* To clean the directories, run:
  * `make clean`
  
## Examples that you can use to test the service, just add them in the `test` target in the Makefile:
```
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl

`Output:`
[
  "total 44",
  "drwxrwxr-x 4 spathan spathan 4096 Feb 14 19:23 build",
  "drwxrwxr-x 2 spathan spathan 4096 Feb 14 19:23 dist",
  "-rw-rw-r-- 1 spathan spathan  244 Feb 14 19:21 Dockerfile",
  "-rw-rw-r-- 1 spathan spathan 1662 Feb 14 19:21 git_push.sh",
  "-rw-rw-r-- 1 spathan spathan 1111 Feb 14 19:21 README.md",
  "-rw-rw-r-- 1 spathan spathan   84 Feb 14 19:21 requirements.txt",
  "-rw-rw-r-- 1 spathan spathan  829 Feb 14 19:21 setup.py",
  "drwxrwxr-x 6 spathan spathan 4096 Feb 14 19:23 swagger_server",
  "drwxrwxr-x 2 spathan spathan 4096 Feb 14 19:23 swagger_server.egg-info",
  "-rw-rw-r-- 1 spathan spathan   90 Feb 14 19:21 test-requirements.txt",
  "-rw-rw-r-- 1 spathan spathan  149 Feb 14 19:21 tox.ini",
  ""
]
```

```
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/uname%20%2Da

`Output:`
"Linux spathan-VirtualBox 4.13.0-32-generic #35~16.04.1-Ubuntu SMP Thu Jan 25 10:13:43 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux\n"
```

* When you do not give the Authorization header, it throws an error saying: `You have to login with proper credentials`
```
curl -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl
You have to login with proper credentials
```

## Note :
* Since I am using POST, the execution is done via curl.
* Use proper url encoding for commands which have spaces \(for ex: ls -l, uname -a etc\) or other special characters in the curl command.
* This code has been tested only on localhost as of now \(since I did not have any other machine to connect to\).
* Use the correct base64 encoded string in the header for the authentication.
* Since I'm using ssh to connect to the hostname, it waits for the authentication to execute the command, make sure to enter your password on the server-side.

## TODO :
* passwordless ssh
* Generate Client-side code.

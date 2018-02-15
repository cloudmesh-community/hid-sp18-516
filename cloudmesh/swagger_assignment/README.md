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

## Execution Details :
* git clone the project
* go to the flaskConnexion directory using `cd`
* Run the following commands one by one:
  * pip install -r requirements.txt
  * python setup.py install
  * python -m swagger_server
* You should see a message like this:
  ``` 
  Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
  ```
* While the server is running, open another terminal and run the following curl command: 
    * for example: `ls -l` command
```
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "<username>", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl
```

## Examples :
```
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl
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
curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ssh/uname%20%2Da
"Linux spathan-VirtualBox 4.13.0-32-generic #35~16.04.1-Ubuntu SMP Thu Jan 25 10:13:43 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux\n"
```

## Note :
* Since I am using POST, the execution is done via curl.
* Use proper url encoding for commands which have spaces \(for ex: ls -l, uname -a etc\) or other special characters in the curl command.
* I have only tested this on localhost \(since I did not have any other machine to connect to\).
* The username and password for now is `admin` and `secret` respectively. Use the correct base64 encoded string in the header.
* This is not the final code and it will be improved based on the feedback given.

## TODO :
* Generate Client-side code and verify.

.PHONY: all test clean

SWAGGERCODEGEN=java -jar swagger-codegen-cli.jar
YAMLFILE1=localhost.yaml
YAMLFILE2=security.yaml
DESTDIR=server/
CONFIGDIR=~/.cloudmesh/

dest:
	mkdir -p $(DESTDIR)
	mkdir -p $(CONFIGDIR)

service: dest
	$(SWAGGERCODEGEN) generate -i $(YAMLFILE1) -l python-flask -o $(DESTDIR) -D supportPython2=true
	cp -r default_controller.py $(DESTDIR)/swagger_server/controllers
	cp -r auth_util.py $(DESTDIR)/swagger_server/controllers
	cp -r __main__.py $(DESTDIR)/swagger_server/
	cp -r $(YAMLFILE2) $(CONFIGDIR)
	cd $(DESTDIR) && pip install -r requirements.txt && \
        python setup.py install

start: 
	cd $(DESTDIR) && python -m swagger_server

test:
	echo "Executing curl command1 on VM2:"
	curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "sheena", "hostName": "192.168.56.102", "command": "ls -l"}' http://localhost:8080/cloudmesh/localhost
	echo "Executing curl command2 on VM2:"
	curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "sheena", "hostName": "192.168.56.102", "command": "uname -a"}' http://localhost:8080/cloudmesh/localhost
	echo "Executing curl command3 without Basic Auth:"
	curl -H "Content-Type:application/json" -X POST -d '{"userName": "sheena", "hostName": "192.168.56.102", "command": "ls -l"}' http://localhost:8080/cloudmesh/localhost
            
stop:
	ps -ef | grep swagger | grep -v "grep"| awk '{print $$2}' | xargs kill -9

clean:
	rm -r $(DESTDIR)
	rm -r $(CONFIGDIR)

container:
	sudo docker build -t cloudmesh-localhost .
	sudo docker run -p 8080:8080 cloudmesh-localhost 


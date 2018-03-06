SWAGGERCODEGEN=java -jar swagger-codegen-cli.jar
YAMLFILE1=localhost.yaml
YAMLFILE2=security.yaml
DESTDIR=server/
CONFIGDIR=~/.cloudmesh/

dest:
	mkdir $(DESTDIR)
	mkdir $(CONFIGDIR)

service: dest
	$(SWAGGERCODEGEN) generate -i $(YAMLFILE1) -l python-flask -o $(DESTDIR) -D supportPython2=true
	cp -r *.py $(DESTDIR)/swagger_server/controllers
	cp -r $(YAMLFILE2) $(CONFIGDIR)

run: 
	cd $(DESTDIR) && pip install -r requirements.txt && \
	python setup.py install && python -m swagger_server

test:
	echo "Executing curl command1, please enter password:"
	curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl
	echo "Executing curl command2:"
	curl -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl
            
stop:
	ps -ef | grep swagger | grep -v "grep"| awk '{print $$2}' | xargs kill -9

clean:
	rm -r $(DESTDIR)
	rm -r $(CONFIGDIR)

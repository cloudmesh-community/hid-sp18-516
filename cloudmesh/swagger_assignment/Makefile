.PHONY: book images

JARFILE=swagger-codegen-cli.jar
YAMLFILE=localhost.yaml
DESTDIR=server/command/flaskConnexion

dest:
	mkdir -p $(DESTDIR)/creds

service: dest
	java -jar $(JARFILE) generate -i $(YAMLFILE) -l python-flask -o $(DESTDIR) -D supportPython2=true
	cp -r *.py $(DESTDIR)/swagger_server/controllers
	cp -r config.yaml $(DESTDIR)/creds
run: 
	cd $(DESTDIR) && pip install -r requirements.txt && \
	python setup.py install && python -m swagger_server

test:
	curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl
            
stop:
	ps -ef | grep swagger | grep -v "grep"| awk '{print $$2}' | xargs kill -9

clean:
	rm -rf $(DESTDIR)

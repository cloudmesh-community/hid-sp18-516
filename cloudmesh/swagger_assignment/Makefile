.PHONY: book images

JARFILE=swagger-codegen-cli.jar
YAMLFILE=localhost.yaml
TESTPATH=~/
DESTDIR=server/command/flaskConnexion

dest:
	mkdir -p $(DESTDIR)

clean:
	rm -rf $(TESTPATH)($(DESTDIR)) 

service: dest
	java -jar $(JARFILE) generate -i $(YAMLFILE) -l python-flask -o $(DESTDIR) -D supportPython2=true
	cp -r *.py $(DESTDIR)/swagger_server/controllers
run: 
	cd $(DESTDIR) && pip install -r requirements.txt && \
	python setup.py install && python -m swagger_server

test:
	curl -H "Authorization: Basic YWRtaW46c2VjcmV0" -H "Content-Type:application/json" -X POST -d '{"userName": "spathan", "hostName": "localhost"}' http://localhost:8080/api/ls%20%2Dl
            


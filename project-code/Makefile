.PHONY: all test clean

SWAGGERCODEGEN=java -jar swagger-codegen-cli.jar
YAMLFILE1=openstack.yaml
YAMLFILE2=class.yaml
DESTDIR=server/
CONFIGDIR=~/.cloudmesh/

dest:
	mkdir -p $(DESTDIR)
	mkdir -p $(CONFIGDIR)

service: dest
	$(SWAGGERCODEGEN) generate -i $(YAMLFILE1) -l python-flask -o $(DESTDIR) -D supportPython2=true
	cp -r default_controller.py $(DESTDIR)/swagger_server/controllers
	cp -r util.py $(DESTDIR)/swagger_server/controllers
	cp -r __main__.py $(DESTDIR)/swagger_server/
	cp -r $(YAMLFILE2) $(CONFIGDIR)
	cd $(DESTDIR) && pip install -r requirements.txt && \
        python setup.py install

start: 
	cd $(DESTDIR) && python -m swagger_server

stop:
	ps -ef | grep swagger | grep -v "grep"| awk '{print $$2}' | xargs kill -9


clean:
	if [ -d $(DESTDIR) ]; then rm -r $(DESTDIR); fi
	if [ -d $(CONFIGDIR) ]; then rm -r $(CONFIGDIR); fi

test_VMs: 
	echo "List instances:"
	curl -H "Content-Type:application/json" -X GET http://localhost:8080/cloudmesh/openstack/listInstances

test_images: 
	echo "List images:"
	curl -H "Content-Type:application/json" -X GET http://localhost:8080/cloudmesh/openstack/images

test_flavors:	
	echo "List flavors:"
	curl -H "Content-Type:application/json" -X GET http://localhost:8080/cloudmesh/openstack/flavor

test_createVM:
	echo "Create an instance by taking default parameters:"
	curl -H "Content-Type:application/json" -X POST -d '{"instance_name": "test-VM1-516"}' http://localhost:8080/cloudmesh/openstack/createInstance
	echo "Create an instance with the parameters specified:"
	curl -H "Content-Type:application/json" -X POST -d '{"instance_name": "test-VM2-516", "image_id": "1895dc93-7cd8-4b46-a252-4eb55b80859f", "flavor_id": "2", "keypair_name": "openstackVM", "security_group": "default"}' http://localhost:8080/cloudmesh/openstack/createInstance
	
test_secgroup:
	echo "Create Security Group:"
	curl -H "Content-Type:application/json" -X POST -d '{"group_name": "default_test"}' http://localhost:8080/cloudmesh/openstack/securitygroup
	
test_keypair:
	echo "Add SSH Keypair:"
	#curl -H "Content-Type:application/json" -X POST -d '{"keypair_name": "openstackVM", "public_key": "~/.ssh/openstackVM.pub"}' http://localhost:8080/cloudmesh/openstack/addkeypair
	curl -H "Content-Type:application/json" -X POST -d '{"keypair_name": "<keypair name>", "public_key": "<public key file path as shown above>"}' http://localhost:8080/cloudmesh/openstack/addkeypair
	
test_floatingIP:
	echo "Attach Floating IP to the instance:"
	curl -H "Content-Type:application/json" -X POST -d '{"instance_name": "test-VM1-516"}' http://localhost:8080/cloudmesh/openstack/floatingIP
	curl -H "Content-Type:application/json" -X POST -d '{"instance_name": "test-VM2-516"}' http://localhost:8080/cloudmesh/openstack/floatingIP

test_stopVM:
	echo "Stop an instance:"
	curl -H "Content-Type:application/json" -X POST -d '{"instance_name": "test-VM2-516"}' http://localhost:8080/cloudmesh/openstack/stopInstance

test_startVM:
	echo "Start an instance:"
	curl -H "Content-Type:application/json" -X POST -d '{"instance_name": "test-VM2-516"}' http://localhost:8080/cloudmesh/openstack/startInstance

test_deleteVM:
	echo "Delete an instance:"
	curl -H "Content-Type:application/json" -X DELETE http://localhost:8080/cloudmesh/openstack/deleteInstance/test-VM1-516

docker-build:
	docker build -t cloudmesh-openstack .

docker-start:
	docker run -p 8080:8080 cloudmesh-openstack 

docker-start-detach-mode:
	docker run -d -p 8080:8080 cloudmesh-openstack

docker-stop:
	docker stop $$(docker ps -a -q -f status=running)


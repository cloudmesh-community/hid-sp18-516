HOME=/hid-sp18-516/tutorial

dest:
	mkdir -p ~/.cloudmesh/
    
copy: dest
	cp -r cc-openrc.sh ~/.cloudmesh/

build:
	sudo docker build -t openstack-tutorial .

run:
	sudo docker run -p 8080:8080 --rm -it openstack-tutorial bash



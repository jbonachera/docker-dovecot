all: build test
build:
	docker build -t docker.io/jbonachera/dovecot . 
test:
	cd tests && tox

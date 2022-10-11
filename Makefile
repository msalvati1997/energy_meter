help:

all:    
	make build
	make test
build:
    @echo "Starting sensors over the host machines"
	docker-compose -f /host_sensors/docker-compose.yaml up 
test:
    @echo "Starting tests"
	docker-compose -f /test/docker-compose.yaml up 
clean: 
    @echo "Removing docker's images"
	docker-compose -f /host_sensors/docker-compose.yaml down
	docker-compose -f /test/docker-compose.yaml down 

%:
	@echo Available targets:
	@echo "  help"
	@echo "  clean"
	@echo "  test"
	@echo "  build"
	@echo "  all"

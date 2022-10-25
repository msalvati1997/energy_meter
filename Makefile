path := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
cwd  := $(shell pwd)

help:


test-parallel-containers:
	docker compose -f $(path)/test/docker-compose.yaml up --remove-orphans
	@echo "Test finished"

start-sensors:
	docker compose -f $(path)/host_sensors/docker-compose.yaml up  

test-cpus:
	docker compose -f $(path)/test/docker-compose-cpus.yaml up 
	@echo "Test finished"	

clean-test-cpus:
	docker compose -f $(path)/test/docker-compose-cpus.yaml down

clean-all:
	@echo "Removing docker's images"
	docker compose -f $(path)/host_sensors/docker-compose.yaml down 
	docker compose -f $(path)/test/docker-compose.yaml down 

clean-test:
	@echo "Removing docker's images of test's container"
	docker compose -f $(path)/test/docker-compose.yaml down 

%:
	@echo Available targets:
	@echo "  help"
	@echo "  clean-all"
	@echo "  clean-test"
	@echo "  test-parallel-containers"
	@echo "  test-cpus"
	@echo "  clean-test-cpus"
	@echo "  start-sensors"


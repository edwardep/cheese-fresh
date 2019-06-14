TEST_YML = docker-compose.test.yml
DEV_YML = docker-compose.yml

clear_cache:
	sudo rm -rf application/.pytest_cache
	sudo rm -rf application/app_logic/__pycache__
	sudo rm -rf application/tests/__pycache__
	sudo rm -rf authentication/.pytest_cache
	sudo rm -rf authentication/auth/__pycache__
	sudo rm -rf authentication/tests/__pycache__
	sudo rm -rf storage/.pytest_cache
	sudo rm -rf storage/server/__pycache__
	sudo rm -rf storage/tests/__pycache__

dev: clear_cache
	docker-compose -f $(DEV_YML) up --build

test_build: clear_cache
	docker-compose -f $(TEST_YML) build

test_up:
	@#docker-compose -f $(TEST_YML) up
	# docker-compose -f $(TEST_YML) run authentication
	docker-compose -f $(TEST_YML) run application
	#docker-compose -f $(TEST_YML) run storage_server
	@#docker logs --tail 100 app_test -f
	@#docker logs --tail 10 auth_test -f
	@docker stop mongo_test
	@docker stop cheese-fresh_zookeeper_1
	@# docker stop storage_test

test_storage:
	docker-compose -f $(TEST_YML) run storage_server

rm_containers:
	docker rm mongo_test
	docker rm storage_test
help:
	@echo test_up 	: docker-compose-test up
	@echo test_build: docker-compose-test up --build
	@echo dev		: docker-compose up --build
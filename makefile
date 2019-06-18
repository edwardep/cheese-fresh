DC = docker-compose

TEST_YML = -f docker-compose.test.yml
DEV_YML = -f docker-compose.yml

DBG_MODE = 1
ifeq ($(DBG_MODE),1)
	VERBOSE = -v
	STD_OUT = -s
else
	VERBOSE =
	STD_OUT =
endif

# disable caching in dev & test mode, issues with mounted dir
# disable warnings, known issue with mongoengine Driver
PYT_BASIC_FLAGS = -p no:cacheprovider -p no:warnings
PYT_FLAGS = $(VERBOSE) $(STD_OUT) $(PYT_BASIC_FLAGS)

PYTEST = python -m pytest
dev: clear_cache
	docker-compose -f $(DEV_YML) up --build

test_build: clear_cache
	docker-compose $(TEST_YML) build

REMOVE_AFTER = --rm

APPLICATION = $(REMOVE_AFTER) application
AUTHENTICATION = $(REMOVE_AFTER) authentication

STOP_MONGO = docker stop cheese-fresh_mongodb_1
STOP_ZK = docker stop cheese-fresh_zookeeper_1


test: te
ISOLATED = 1
ifeq ($(ISOLATED), 1)
	STOP_SERVICES = docker stop cheese-fresh_mongodb_1 && docker stop cheese-fresh_zookeeper_1
else
	STOP_SERVICES =
endif

stop_services:
	@docker stop cheese-fresh_mongodb_1
	@docker stop cheese-fresh_zookeeper_1

test_app: 			run_test_app stop_services
test_auth: 			run_test_auth stop_services
test_storage: 		run_test_storage stop_services
test_all_storages: 	run_test_all_storages stop_services
test_all:			run_test_app
					run_test_auth
					stop_services
run_test_app:
	@$(DC) $(TEST_YML) run $(APPLICATION) $(PYTEST) $(PYT_FLAGS)

run_test_auth:
	@$(DC) $(TEST_YML) run $(AUTHENTICATION) $(PYTEST) $(PYT_FLAGS)

run_test_storage:
	@$(DC) $(TEST_YML) run storage_server_0 $(PYTEST) $(PYT_FLAGS)

run_test_all_storages:
	@$(DC) $(TEST_YML) run storage_server_0 $(PYTEST) $(PYT_FLAGS)
	@$(DC) $(TEST_YML) run storage_server_1 $(PYTEST) $(PYT_FLAGS)
	@$(DC) $(TEST_YML) run storage_server_2 $(PYTEST) $(PYT_FLAGS)
	@$(DC) $(TEST_YML) run storage_server_3 $(PYTEST) $(PYT_FLAGS)

	


rm_containers:
	docker rm mongo_test
	docker rm storage_test
help:
	@echo test_up 	: docker-compose-test up
	@echo test_build: docker-compose-test up --build
	@echo dev		: docker-compose up --build

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

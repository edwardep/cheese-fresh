.DEFAULT_GOAL:=help
DC = docker-compose

TEST_YML = -f docker-compose.test.yml
DEV_YML = -f docker-compose.yml

# Pytest Optional flags
DBG_MODE = 1
ifeq ($(DBG_MODE),1)
	VERBOSE = -v
	STD_OUT = -s
else
	VERBOSE =
	STD_OUT =
endif

# disable caching in dev & test mode because of issues with mounted dir
# disable warnings, known issue with mongoengine Driver
PYT_BASIC_FLAGS = -p no:cacheprovider -p no:warnings
PYT_FLAGS = $(VERBOSE) $(STD_OUT) $(PYT_BASIC_FLAGS)

PYTEST = python -m pytest
REMOVE_AFTER = --rm

APPLICATION = $(REMOVE_AFTER) application
AUTHENTICATION = $(REMOVE_AFTER) authentication
STORAGE_0 = $(REMOVE_AFTER) storage_server_0
STORAGE_1 = $(REMOVE_AFTER) storage_server_1
STORAGE_2 = $(REMOVE_AFTER) storage_server_2
STORAGE_3 = $(REMOVE_AFTER) storage_server_3

##@ Testing
.PHONY: test_web test_app test_auth test_storage test_all
test_web:														## run web's tests
test_app: 			run_test_app stop_services					## run application's tests (37)
test_auth: 			run_test_auth stop_services					## run authentication's tests (11)
test_storage: 		run_test_storage stop_services				## run storage's tests (4)
test_all:			run_test_app run_test_auth stop_services	## run all of the above
										
run_test_app:
	@$(DC) $(TEST_YML) run $(APPLICATION) $(PYTEST) $(PYT_FLAGS)

run_test_auth:
	@$(DC) $(TEST_YML) run $(AUTHENTICATION) $(PYTEST) $(PYT_FLAGS)

run_test_storage:
	@$(DC) $(TEST_YML) run $(STORAGE_0) $(PYTEST) $(PYT_FLAGS)

run_test_all_storages:
	@$(DC) $(TEST_YML) run $(STORAGE_0) $(PYTEST) $(PYT_FLAGS)
	@$(DC) $(TEST_YML) run $(STORAGE_1) $(PYTEST) $(PYT_FLAGS)
	@$(DC) $(TEST_YML) run $(STORAGE_2) $(PYTEST) $(PYT_FLAGS)
	@$(DC) $(TEST_YML) run $(STORAGE_3) $(PYTEST) $(PYT_FLAGS)

stop_services:
	@docker stop cheese-fresh_mongodb_1
	@docker stop cheese-fresh_zookeeper_1

build_tests: clear_cache				## Build all testing containers
	@$(DC) $(TEST_YML) build

##@ Run Mode
dev: clear_cache			## docker-compose up --build
	docker-compose -f $(DEV_YML) up --build




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

##@ Helpers
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
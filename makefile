clear_cache:
	sudo rm -rf application/.pytest_cache
	sudo rm -rf application/app_logic/__pycache__
	sudo rm -rf application/tests/__pycache__
	sudo rm -rf authentication/.pytest_cache
	sudo rm -rf authentication/auth/__pycache__
	sudo rm -rf authentication/tests/__pycache__

dev: clear_cache
	docker-compose up --build

test_build: clear_cache
	docker-compose -f docker-compose.test.yml build

test_up:
	docker-compose -f docker-compose.test.yml up
	#docker logs --tail 100 app_test -f
	#docker logs --tail 10 auth_test -f

help:
	@echo test_up 	: docker-compose-test up
	@echo test_build: docker-compose-test up --build
	@echo dev		: docker-compose up --build
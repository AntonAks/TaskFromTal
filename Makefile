.PHONY: install-pre-commit run-pre-commit

setup-local-env:
	pip install pre-commit
	pre-commit install

run-pre-commit:
	pre-commit run --all-files



restart:
	docker-compose down
	docker-compose build
	docker-compose up

run:
	docker-compose stop
	docker-compose up

stop:
	docker-compose stop

down:
	docker-compose down

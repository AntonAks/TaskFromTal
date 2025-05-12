.PHONY: install-pre-commit run-pre-commit

setup-local-env:
	pip install -r requirements.txt
	pre-commit install

run-pre-commit:
	pre-commit run --all-files

start:
	docker-compose -f docker-compose.yaml  up --build
	docker-compose up


restart:
	docker-compose down
	docker-compose -f docker-compose.yaml  up --build
	docker-compose up


start-prod:
	docker-compose -f docker-compose-prod.yaml  up --build
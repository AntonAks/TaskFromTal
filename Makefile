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

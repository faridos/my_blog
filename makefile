test:
	docker-compose run --rm app  python manage.py test
run-prod: #prod env
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up
run-dev: # dev env
	docker-compose  up
makemigrations:
	docker-compose run --rm app  python manage.py makemigrations
migrate:
	docker-compose run --rm app  python manage.py migrate
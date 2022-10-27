test:
	docker-compose run --rm app python3 manage.py test # needed this way so it can spin up a DB along with app service.
run-prod: #prod env
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up
run-dev: # dev env
	docker-compose  up --build
make-migrations:
	docker-compose run --rm app  python manage.py makemigrations
migrate:
	docker-compose run --rm app  python manage.py migrate
createsuperuser:
	docker-compose run --rm app python manage.py createsuperuser
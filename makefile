test:
	docker-compose run --rm app python3 manage.py test # needed this way so it can spin up a DB along with app service.

run: # dev env
	docker-compose  up
make-migrations:
	docker-compose run --rm app  python manage.py makemigrations
migrate:
	docker-compose run --rm app  python manage.py migrate

createsuperuser:
	docker-compose run --rm app python manage.py createsuperuser

collectstatic:
	docker-compose run --rm app python3 manage.py collectstatic


run-prod: #prod env
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml  build app && docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up
make-migrations-prod:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml run --rm app  python manage.py makemigrations
migrate-prod:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml run --rm app  python manage.py migrate
createsuperuser-prod:
	docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml run --rm app python manage.py createsuperuser
collectstatic-prod:
	docker-compose run --rm app python3 manage.py collectstatic
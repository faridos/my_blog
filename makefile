test-gitlab-ci:
	virtualenv -p python3.7 .venv && . .venv/bin/activate && pip3 install -r requirements/dev.in && python3 manage.py test
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
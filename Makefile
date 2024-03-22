.PHONY: install
install:
	poetry install

.PHONY: migrations
migrations:
	poetry run python mediamajesty/manage.py makemigrations

.PHONY: migrate
migrate:
	poetry run python mediamajesty/manage.py migrate

.PHONY: run
run:
	poetry run python mediamajesty/manage.py runserver

.PHONY: superuser
superuser:
	poetry run python mediamajesty/manage.py createsuperuser

.PHONY: start
start: install migrations migrate run

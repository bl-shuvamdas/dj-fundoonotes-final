py = python manage.py

test:
	@pytest

migrate:
	@$(py) makemigrations
	@$(py) migrate

run: migrate test
	@$(py) runserver

runpika:
	@$(py) runpika

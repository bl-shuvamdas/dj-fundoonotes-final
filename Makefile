py = python manage.py

test:
	@pytest

migrate:
	@$(py) makemigrations
	@$(py) migrate

run: migrate
	@$(py) runserver

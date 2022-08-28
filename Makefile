py = python manage.py

migrate:
	$(py) makemigrations
	$(py) migrate

run: migrate
	$(py) runserver

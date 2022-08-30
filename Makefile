py = python manage.py

test:
	@pytest

migrate:
	@$(py) makemigrations
	@$(py) migrate

run: migrate test
	@$(py) runserver


celery:
	@celery -A core worker -l INFO --pool=solo

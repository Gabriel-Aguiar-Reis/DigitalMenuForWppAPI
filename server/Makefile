.PHONY: format install manage_migrations security serve serve_doc test

format:
	@isort .
	@blue .
install:
	@poetry install
manage_migrations:
	@py manage.py makemigrations
	@py manage.py migrate
security:
	@pip-audit
serve:
	@py manage.py runserver 8000
serve_doc:
	@mkdocs serve --dev-addr '127.0.0.1:8001'
test:
	@pytest -v
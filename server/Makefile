.PHONY: doc_server format install manage_migrations security server test

doc_server:
	@mkdocs serve --dev-addr '127.0.0.1:8001'
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
server:
	@py manage.py runserver 8000
test:
	@pytest -v
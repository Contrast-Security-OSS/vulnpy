templates:
	./scripts/gen_templates.sh

flask: templates
	FLASK_APP=apps/flask_app.py flask run --port=8000

falcon: templates
	gunicorn apps.falcon_app:app

pyramid: templates
	python apps/pyramid_app.py

django: templates
	python apps/django_app.py runserver

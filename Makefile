HOST ?= localhost
PORT ?= 8000
UWSGI_OPTIONS := --enable-threads --single-interpreter --http $(HOST):$(PORT)
GUNICORN_OPTIONS := --timeout=0 -b $(HOST):$(PORT)

export VULNPY_REAL_SSRF_REQUESTS = true

templates:
	./scripts/gen_templates.sh

flask: templates
	FLASK_APP=apps/flask_app.py flask run --host=$(HOST) --port=$(PORT)

flask-two-apps: templates
	FLASK_APP=apps/flask_two_apps.py:combined_app flask run --host=$(HOST) --port=$(PORT)

# note: vulnpy's routing strategy for falcon is quite nonstandard
falcon: templates
	gunicorn $(GUNICORN_OPTIONS) apps.falcon_app:app

falcon-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.falcon_app:app

flask-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.flask_app:app

flask-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.flask_app:app

pyramid: templates
	python apps/pyramid_app.py $(HOST):$(PORT)

pyramid-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.pyramid_app:app

pyramid-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.pyramid_app:app

django: templates
	python apps/django_app.py runserver --noreload $(HOST):$(PORT)

django-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.django_app:application

django-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.django_app:application

wsgi: templates
	python apps/wsgi_app.py $(HOST) $(PORT)

wsgi-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.wsgi_app:app

wsgi-two-apps: templates
	python apps/wsgi_two_apps.py $(HOST) $(PORT)

wsgi-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.wsgi_app:app

bottle: templates
	python apps/bottle_app.py $(HOST) $(PORT)

bottle-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.bottle_app:app

bottle-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.bottle_app:app

fastapi: templates
	uvicorn apps.fastapi_app:app --host=$(HOST) --port=$(PORT)

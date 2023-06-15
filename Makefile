HOST ?= localhost
PORT ?= 8000
UWSGI_OPTIONS := --enable-threads --single-interpreter --master --lazy-apps --http $(HOST):$(PORT) --honour-stdin
GUNICORN_OPTIONS := --timeout=0 -b $(HOST):$(PORT)

export VULNPY_REAL_SSRF_REQUESTS = true

templates:
	./scripts/gen_templates.sh

falcon: # falcon has no default server, so we use gunicorn
	$(error Falcon requires a production webserver - try `make falcon-gunicorn`)

falcon-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.falcon_app:app

# note: vulnpy's routing strategy for falcon is quite nonstandard
falcon-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.falcon_app:app

falcon-asgi: # falcon has no default server, so we use uvicorn
	$(error Falcon ASGI requires a production webserver - try `make falcon-uvicorn`)

falcon-uvicorn: templates
	uvicorn apps.falcon_asgi_app:app --host=$(HOST) --port=$(PORT)

flask: templates
	FLASK_APP=apps/flask_app.py flask run --host=$(HOST) --port=$(PORT)

flask-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.flask_app:app

flask-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.flask_app:app

flask-two-apps: templates
	FLASK_APP=apps/flask_two_apps.py:combined_app flask run --host=$(HOST) --port=$(PORT)

pyramid: templates
	python apps/pyramid_app.py $(HOST):$(PORT)

pyramid-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.pyramid_app:app

pyramid-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.pyramid_app:app

django: templates
	python apps/django_app.py runserver --noreload $(HOST):$(PORT)

django-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.django_app:vulnpy_app

django-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.django_app:vulnpy_app

django-asgi: # django has no default server, so we use uvicorn
	$(error Django ASGI  requires a production webserver - try `make django-uvicorn`)

django-uvicorn: templates
	uvicorn apps.django_asgi_app:vulnpy_app --host $(HOST) --port $(PORT)

wsgi: templates
	python apps/wsgi_app.py $(HOST) $(PORT)

wsgi-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.wsgi_app:app

wsgi-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.wsgi_app:app

wsgi-two-apps: templates
	python apps/wsgi_two_apps.py $(HOST) $(PORT)

bottle: templates
	python apps/bottle_app.py $(HOST) $(PORT)

bottle-uwsgi: templates
	uwsgi $(UWSGI_OPTIONS) -w apps.bottle_app:app

bottle-gunicorn: templates
	gunicorn $(GUNICORN_OPTIONS) apps.bottle_app:app

fastapi: templates
	uvicorn apps.fastapi_app:app --host=$(HOST) --port=$(PORT)

aiohttp: templates
	python -m aiohttp.web -H $(HOST) -P $(PORT) apps.aiohttp_app:init_app

quart: templates
	python apps/quart_app.py $(HOST) $(PORT)

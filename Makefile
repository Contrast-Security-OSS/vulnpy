HOST ?= localhost
PORT ?= 8000

export VULNPY_REAL_SSRF_REQUESTS = true

templates:
	./scripts/gen_templates.sh

flask: templates
	FLASK_APP=apps/flask_app.py flask run --host=$(HOST) --port=$(PORT)

flask-two-apps: templates
	FLASK_APP=apps/flask_two_apps.py:combined_app flask run --host=$(HOST) --port=$(PORT)

falcon: templates
	gunicorn -b $(HOST):$(PORT) --timeout=0 apps.falcon_app:app

falcon-uwsgi: templates
	uwsgi -w apps.falcon_app:app --enable-threads --single-interpreter --http $(HOST):$(PORT)

pyramid: templates
	python apps/pyramid_app.py $(HOST):$(PORT)

django: templates
	python apps/django_app.py runserver $(HOST):$(PORT)

wsgi: templates
	python apps/wsgi_app.py $(HOST) $(PORT)

wsgi-two-apps: templates
	python apps/wsgi_two_apps.py $(HOST) $(PORT)

bottle: templates
	python apps/bottle_app.py $(HOST) $(PORT)


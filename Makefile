HOST ?= localhost
PORT ?= 8000

export VULNPY_REAL_SSRF_REQUESTS = true

templates:
	./scripts/gen_templates.sh

flask: templates
	FLASK_APP=apps/flask_app.py flask run --host=$(HOST) --port=$(PORT)

falcon: templates
	gunicorn -b $(HOST):$(PORT) apps.falcon_app:app

pyramid: templates
	python apps/pyramid_app.py $(HOST):$(PORT)

django: templates
	python apps/django_app.py runserver $(HOST):$(PORT)

wsgi: templates
	python apps/wsgi_app.py $(HOST) $(PORT)

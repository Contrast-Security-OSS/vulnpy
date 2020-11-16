HOST ?= localhost
PORT ?= 8000

templates:
	./scripts/gen_templates.sh

flask: templates
	VULNPY_REAL_SSRF_REQUESTS=true FLASK_APP=apps/flask_app.py flask run --host=$(HOST) --port=$(PORT)

falcon: templates
	VULNPY_REAL_SSRF_REQUESTS=true gunicorn -b $(HOST):$(PORT) apps.falcon_app:app

pyramid: templates
	VULNPY_REAL_SSRF_REQUESTS=true python apps/pyramid_app.py $(HOST):$(PORT)

django: templates
	VULNPY_REAL_SSRF_REQUESTS=true python apps/django_app.py runserver $(HOST):$(PORT)

wsgi: templates
	VULNPY_REAL_SSRF_REQUESTS=true python apps/wsgi_app.py $(HOST) $(PORT)

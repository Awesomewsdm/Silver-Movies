PYTHON=python
COMPOSE=docker compose

.PHONY: up migrate test e2e

up:
	$(COMPOSE) up -d

migrate:
	$(COMPOSE) run --rm web $(PYTHON) project_nexus/manage.py migrate

test:
	$(COMPOSE) run --rm web $(PYTHON) -m coverage run --source='.' project_nexus/manage.py test -v 2
	$(COMPOSE) run --rm web $(PYTHON) -m coverage report -m

e2e:
	# Basic e2e smoke tests against running server
	curl -sS http://localhost:8000/api/movies/trending/ | jq . || true

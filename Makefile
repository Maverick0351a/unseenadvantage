SHELL := /bin/bash

PY := python
VE := .venv

.PHONY: help
help:
	@echo "Targets:"
	@echo "  venv          Create local virtualenv"
	@echo "  install       Install package with dev+ui extras"
	@echo "  test          Run pytest"
	@echo "  demo          Run synthetic demo -> reports/"
	@echo "  api           Run API locally on :8088"
	@echo "  smoke         Run API smoke script (starts & checks server)"
	@echo "  docker-build  Build Docker image"
	@echo "  docker-run    Run Docker API container"
	@echo "  compose-up    docker compose up -d"
	@echo "  compose-down  docker compose down"

$(VE)/bin/activate:
	$(PY) -m venv $(VE)

venv: $(VE)/bin/activate

install: venv
	$(VE)/bin/pip install --upgrade pip
	$(VE)/bin/pip install -e ".[dev,ui]"

test:
	$(VE)/bin/pytest -q

demo:
	$(VE)/bin/python scripts/run_demo.py

api:
	$(VE)/bin/python -m uvicorn unseen_advantage.api.server:app --host 0.0.0.0 --port 8088

smoke:
	$(VE)/bin/python scripts/api_smoke.py

docker-build:
	docker build -t unseen-advantage:local .

docker-run:
	docker run --rm -it -p 8088:8088 -v $$PWD/reports:/app/reports unseen-advantage:local

compose-up:
	docker compose up -d --build

compose-down:
	docker compose down

# Windows note: Use make via Git Bash or WSL. Otherwise run commands directly.

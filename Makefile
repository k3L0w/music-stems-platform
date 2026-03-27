SHELL := /bin/bash

.PHONY: up down logs web-install api-install worker-install web-dev api-run worker-run

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

web-install:
	cd apps/web && npm install

api-install:
	cd services/api && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

worker-install:
	cd services/worker && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt

web-dev:
	cd apps/web && npm run dev

api-run:
	cd services/api && . .venv/bin/activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

worker-run:
	cd services/worker && . .venv/bin/activate && python -m app.main

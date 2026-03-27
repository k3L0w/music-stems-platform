SHELL := /bin/bash

.PHONY: up down logs web-install api-install worker-install

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

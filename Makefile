.PHONY: install run run-sim run-api test lint format up down

install:
	pip install -e ".[dev]"

# Runs both services locally via Docker Compose.
run:
	docker compose up --build

run-sim:
	python scripts/run_sim_plant.py

run-api:
	python scripts/run_api.py

test:
	pytest

lint:
	ruff check src tests scripts
	mypy src

format:
	ruff format src tests scripts
	ruff check --fix src tests scripts

up:
	docker compose up -d --build

down:
	docker compose down

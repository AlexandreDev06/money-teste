init:
	cp .env.example .env

install:
	poetry install

docker-up:
	docker compose -d up

docker-down:
	docker compose -d down

run:
	poetry run uvicorn app:app

terminal:
	docker compose exec -it money bash

clean:
	rm -rf .venv __pycache__ .pytest_cache .coverage .mypy_cache

.DEFAULT_GOAL := help

# Help command
help:
	@echo "Available targets:"
	@echo "  init        - Initialize the project"
	@echo "  install     - Install project dependencies"
	@echo "  run         - Run the FastAPI application"
	@echo "  terminal    - Run the terminal in the container"
	@echo "  clean       - Clean up virtual environment and generated files"
	@echo "  help        - Show this help message"
	@echo "  docker-up   - Start the docker compose stack"
	@echo "  docker-down - Stop the docker compose stack"
	
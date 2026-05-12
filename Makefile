.PHONY: install start test build lint format clean help

install:
	pip install -e ".[dev]"

start:
	python -m main

test:
	pytest tests/ -v

lint:
	flake8 . --exclude=__pycache__,*.egg-info
	mypy main.py interfaz/ motor_regex.py patrones.py

format:
	black main.py interfaz/ motor_regex.py patrones.py

build:
	pip install build
	python -m build

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf dist/ build/ htmlcov/

dev:
	pip install watchdog
	watchmedo auto-restart --patterns="*.py" --recursive -- python main.py

help:
	@echo "Comandos disponibles"
	@echo " make install		- Instala Dependencias"
	@echo " make start			- Inicia la aplicación"
	@echo " make dev			- Inicia con auto-reload"
	@echo " make test			- Ejecuta los tests"
	@echo " make lint			- Verifica el código"
	@echo " make format 		- Formatea el código"
	@echo " make build 			- Genera el paquete"
	@echo " make clean			- Limpia archivos temporales"
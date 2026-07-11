.PHONY: install test lint format help

install:  ## Instala as dependencias
	pip install -r requirements.txt

test:  ## Roda a suite de testes via tox
	tox

lint:  ## Roda black + flake8 via tox (o env de lint)
	tox -e lint

format:  ## Formata o codigo com black
	black src tests

help:  ## Lista os alvos disponiveis
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-10s %s\n", $$1, $$2}'

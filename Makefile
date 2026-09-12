.PHONY: build install test coverage docker

build:
	python -m build

install:
	python -m pip install -e .

test:
	pytest -q

coverage:
	coverage run -m pytest || true
	coverage xml || true
	coverage-badge -o coverage.svg || true

docker:
	docker build -t poc-agents-orchestration:latest .

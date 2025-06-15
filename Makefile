.PHONY: test test-e2e

test:
	pip install -r requirements.txt
	python -m pytest

test-e2e:
	pytest -m integration tests/integration/

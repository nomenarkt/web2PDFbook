.PHONY: test test-e2e

test:
	pytest

test-e2e:
	pytest -m integration tests/integration/

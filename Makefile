PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

validate:
	$(PYTHON) -m source_engine validate

audit:
	$(PYTHON) -m source_engine audit

reconcile:
	$(PYTHON) -m source_engine reconcile

generate:
	$(PYTHON) -m source_engine generate --all

determinism:
	$(PYTHON) -m source_engine test-determinism

.PHONY: install test validate audit reconcile generate determinism

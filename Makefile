PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

audit:
	$(PYTHON) -m source_engine audit

reconcile:
	$(PYTHON) -m source_engine reconcile

generate:
	$(PYTHON) -m source_engine generate --all

VIRTUALENV_ROOT := $(shell [ -z $$VIRTUAL_ENV ] && echo $$(pwd)/venv || echo $$VIRTUAL_ENV)

.PHONY: virtualenv
virtualenv:
	[ -z $$VIRTUAL_ENV ] && [ ! -d venv ] && python3 -m venv venv || true

.PHONY: upgrade-pip
## Upgrade pip
upgrade-pip: virtualenv
	${VIRTUALENV_ROOT}/bin/pip install --upgrade pip

.PHONY: requirements
## Install Python requirements for this app
requirements: virtualenv upgrade-pip requirements.txt
	${VIRTUALENV_ROOT}/bin/pip install -r requirements.txt

.PHONY: requirements-dev
## Install Python development requirements for this app
requirements-dev: virtualenv upgrade-pip requirements.txt requirements-dev.txt
	${VIRTUALENV_ROOT}/bin/pip install -r requirements.txt -r requirements-dev.txt

.PHONY: freeze-requirements
## Update the Python requirements*.txt files
freeze-requirements: virtualenv requirements-dev requirements.in requirements-dev.in
	${VIRTUALENV_ROOT}/bin/pip-compile requirements.in
	${VIRTUALENV_ROOT}/bin/pip-compile requirements-dev.in

.PHONY: test-python
## Run Python unit tests
test-python: virtualenv requirements-dev
	${VIRTUALENV_ROOT}/bin/py.test ${PYTEST_ARGS}

.PHONY: test-flake8
## Run Python linter
test-flake8: virtualenv requirements-dev
	${VIRTUALENV_ROOT}/bin/flake8 .

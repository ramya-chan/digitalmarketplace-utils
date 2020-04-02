SHELL := /bin/bash
MAKEFILEDIR := ./Makefiles

include $(MAKEFILEDIR)/include/python.Makefile

.DEFAULT_GOAL := run-all

.PHONY: run-all
run-all: requirements run-app

.PHONY: run-app
run-app: virtualenv
	${VIRTUALENV_ROOT}/bin/flask run

.PHONY: test
test: test-flake8 test-python

.PHONY: docker-%
docker-%:
	@$(MAKE) -f $(MAKEFILEDIR)/include/docker.Makefile $@

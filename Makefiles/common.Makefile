SHELL := /bin/bash
MAKEFILEDIR := ./Makefiles

include $(MAKEFILEDIR)/include/python.Makefile

.DEFAULT_GOAL := run-all

.PHONY: run-app
run-app: show-environment virtualenv
	${VIRTUALENV_ROOT}/bin/flask run

.PHONY: show-environment
show-environment:
	@echo "Environment variables in use:"
	@env | grep DM_ || true

docker-%:
	@$(MAKE) -f $(MAKEFILEDIR)/include/docker.Makefile $@

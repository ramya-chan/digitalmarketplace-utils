SHELL := /bin/bash
MAKEFILEDIR := ./Makefiles

include $(MAKEFILEDIR)/include/python.Makefile

.DEFAULT_GOAL := run-all

DM_ENVIRONMENT ?= development

ifeq ($(DM_ENVIRONMENT),development)
	GULP_ENVIRONMENT := development
else
	GULP_ENVIRONMENT := production
endif

.PHONY: run-all
run-all: requirements npm-install frontend-build run-app

.PHONY: run-app
run-app: show-environment virtualenv
	${VIRTUALENV_ROOT}/bin/flask run

.PHONY: npm-install
npm-install:
	npm ci # If dependencies in the package lock do not match those in package.json, npm ci will exit with an error, instead of updating the package lock. (https://docs.npmjs.com/cli/ci.html)

.PHONY: frontend-build
frontend-build: npm-install
	npm run --silent frontend-build:${GULP_ENVIRONMENT}

.PHONY: test
test: show-environment frontend-build test-flake8 test-python test-javascript

.PHONY: test-javascript
test-javascript: frontend-build
	npm test

.PHONY: show-environment
show-environment:
	@echo "Environment variables in use:"
	@env | grep DM_ || true

.PHONY: docker-%
docker-%:
	@$(MAKE) -f $(MAKEFILEDIR)/include/docker.Makefile $@

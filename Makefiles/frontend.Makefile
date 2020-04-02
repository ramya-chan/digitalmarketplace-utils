MAKEFILEDIR := ./Makefiles

include $(MAKEFILEDIR)/common.Makefile

DM_ENVIRONMENT ?= development

ifeq ($(DM_ENVIRONMENT),development)
	GULP_ENVIRONMENT := development
else
	GULP_ENVIRONMENT := production
endif

.PHONY: run-all
run-all: requirements npm-install frontend-build run-app

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

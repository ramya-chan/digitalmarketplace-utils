MAKEFILEDIR := ./Makefiles

include $(MAKEFILEDIR)/common.Makefile

.PHONY: run-all
## Install everything and run the app
run-all: requirements run-app

.PHONY: test
## Test everything
test: test-flake8 test-python

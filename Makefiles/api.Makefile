MAKEFILEDIR := ./Makefiles

include $(MAKEFILEDIR)/common.Makefile

.PHONY: run-all
run-all: requirements run-app

.PHONY: test
test: test-flake8 test-python

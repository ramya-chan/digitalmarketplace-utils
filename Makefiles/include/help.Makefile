MAKEFILEDIR := Makefiles

HELP_INCLUDE := \
	$(MAKEFILEDIR)/include/docker.Makefile

.PHONY: help

## Print this help message
help:
	$(eval HELP_MAKEFILE_LIST := $(MAKEFILE_LIST) $(HELP_INCLUDE))
	
	$(info Available targets)
	@awk '/^[a-zA-Z\-\_0-9]+:/ {					\
		nb = sub( /^## /, "", helpMsg );			\
		if(nb == 0) {						\
			helpMsg = $$0;					\
			nb = sub( /^[^:]*:.* ## /, "", helpMsg );	\
		}							\
		if (nb)							\
			print  $$1 "\t" helpMsg;			\
	}								\
	{ helpMsg = $$0 }'						\
	$(HELP_MAKEFILE_LIST)						\
	| column -ts $$'\t' | sort -d | grep --color '^[^ ]*'

## Print all available targets
list-targets:
	$(eval HELP_MAKEFILE_LIST := $(MAKEFILE_LIST) $(HELP_INCLUDE))
	
	$(info Available targets)
	@awk ' 								\
	FNR==1 { print "" ; print FILENAME }				\
	/^[a-zA-Z\-\_0-9]+:/ {						\
		nb = sub( /^## /, "", helpMsg );			\
		if(nb == 0) {						\
			helpMsg = $$0;					\
			nb = sub( /^[^:]*:.* ## /, "", helpMsg );	\
		}							\
		if (nb)							\
			print  $$0 "  ## " helpMsg;			\
	}								\
	{ helpMsg = $$0 }'						\
	$(HELP_MAKEFILE_LIST)

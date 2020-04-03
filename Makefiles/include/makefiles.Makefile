MAKEFILEDIR := Makefiles

MAKEFILES_VERSION ?= https://github.com/alphagov/digitalmarketplace-utils.git@master

MAKEFILES_GITREPO := $(word 1, $(subst @, ,$(MAKEFILES_VERSION)))
MAKEFILES_GITTAGS := $(word 2, $(subst @, ,$(MAKEFILES_VERSION)))

.PHONY: makefiles-checkout

## Checkout the common Makefiles from the digitalmarketplace-utils git repo
makefiles-checkout:
	git fetch $(MAKEFILES_GITREPO) $(MAKEFILES_GITTAGS)
	git checkout FETCH_HEAD -- $(MAKEFILEDIR)
	git status $(MAKEFILEDIR)

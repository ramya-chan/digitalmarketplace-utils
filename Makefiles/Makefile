
.PHONY: update-makefile
update-makefile:
	$(eval MAKEFILE_REPO ?= alphagov/digitalmarketplace-utils)
	$(eval MAKEFILE_BRANCH ?= master)
	$(eval MAKEFILE_NAME ?= $(firstword $(subst @, , $(MAKEFILE_VERSION))))
	
	$(eval MAKEFILE_GITREV := $(shell curl -s https://api.github.com/repos/$(MAKEFILE_REPO)/branches/$(MAKEFILE_BRANCH) | jq -r '.commit.sha[0:7]'))
	$(eval MAKEFILE_URL := https://raw.githubusercontent.com/$(MAKEFILE_REPO)/$(MAKEFILE_GITREV))
	
	curl -s $(MAKEFILE_URL)/$(MAKEFILE_NAME) > Makefile
	curl -s $(MAKEFILE_URL)/Makefiles/Makefile >> Makefile
	
	sed -i '' '/MAKEFILE_VERSION/ s/MAKEFILE_GITREV/$(MAKEFILE_GITREV)/' Makefile

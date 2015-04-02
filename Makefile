
PACKAGE = qav
VERSION = $(shell git describe --abbrev=0 --tags)
RELEASE = 1
OS_MAJOR_VERSION = $(shell lsb_release -rs | cut -f1 -d.)
OS := rhel$(OS_MAJOR_VERSION)

ifeq ($(OS),rhel7)
	PYTHON=python
	YUMREPO_LOCATION=/fs/UMyumrepos/rhel7/stable/Packages/noarch
endif
ifeq ($(OS),rhel6)
	PYTHON=python
	YUMREPO_LOCATION=/fs/UMyumrepos/rhel6/stable/Packages/noarch
endif
ifeq ($(OS),rhel5)
	PYTHON=python26
	YUMREPO_LOCATION=/fs/UMyumrepos/rhel5/stable/noarch
endif

REQUIRES := $(PYTHON),$(PYTHON)-netaddr
ifeq ($(OS),rhel5)
	REQUIRES := $(REQUIRES),python26-ordereddict
endif

.PHONY: rpm
rpm:
	$(PYTHON) setup.py bdist_rpm \
		--python=$(PYTHON) \
		--requires=$(REQUIRES)

.PHONY: package
package:
	@echo ================================================================
	@echo cp /fs/UMbuild/$(PACKAGE)/dist/$(PACKAGE)-$(VERSION)-$(RELEASE).noarch.rpm $(YUMREPO_LOCATION)
	@echo createrepo /fs/UMyumrepos/$(OS)/stable

.PHONY: build
build: rpm package



PACKAGE = qav
VERSION = $(shell git describe --tags)
RELEASE = 1
major_version = $(shell lsb_release -rs | cut -f1 -d.)
OS = rhel$(major_version)

ifeq ($(OS),rhel7)
	PYTHON=python
	YUMREPO_LOCATION=/fs/UMyumrepos/rhel7/stable/Packages/noarch
endif
ifeq ($(OS),rhel6)
	PYTHON=python
	YUMREPO_LOCATION=/fs/UMyumrepos/rhel7/stable/Packages/noarch
endif
ifeq ($(OS),rhel5)
	PYTHON=python26
	EXTRA_REQUIRES=$(EXTRA_REQUIRES),python26-ordereddict
	YUMREPO_LOCATION=/fs/UMyumrepos/rhel5/stable/noarch
endif

RPM:
	$(PYTHON) setup.py bdist_rpm --python=$(PYTHON) --requires=$(PYTHON)-netaddr$(EXTRA_REQUIRES)

PACKAGE:
	@echo ================================================================
	@echo cp /fs/UMbuild/$(PACKAGE)/dist/$(PACKAGE)-$(VERSION)-$(RELEASE).noarch.rpm $(YUMREPO_LOCATION)
	@echo createrepo /fs/UMyumrepos/$(OS)/stable

build: RPM PACKAGE


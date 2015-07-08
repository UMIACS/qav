
PACKAGE = qav
VERSION = $(shell git describe --abbrev=0 --tags)
RELEASE = 1
OS_MAJOR_VERSION = $(shell lsb_release -rs | cut -f1 -d.)
OS := rhel$(OS_MAJOR_VERSION)
DIST_DIR := dist/$(OS)

PYTHON=python
ifeq ($(OS),rhel7)
	YUMREPO_LOCATION=/fs/UMyumrepos/rhel7/stable/Packages/noarch
endif
ifeq ($(OS),rhel6)
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
	-mkdir -p $(DIST_DIR)
	$(PYTHON) setup.py bdist_rpm \
			--python=$(PYTHON) \
			--requires=$(REQUIRES) \
			--dist-dir=$(DIST_DIR) \
			--binary-only

.PHONY: package
package:
	@echo ================================================================
	@echo cp /fs/UMbuild/$(PACKAGE)/$(DIST_DIR)/$(PACKAGE)-$(VERSION)-$(RELEASE).noarch.rpm $(YUMREPO_LOCATION)
	@echo createrepo /fs/UMyumrepos/$(OS)/stable

.PHONY: build
build: rpm package

.PHONY: tag
tag:
	sed -i 's/__version__ = .*/__version__ = "$(VERSION)"/g' $(PACKAGE)/__init__.py
	git add $(PACKAGE)/__init__.py
	git commit -m "Tagging $(VERSION)"
	git tag -a $(VERSION) -m "Tagging $(VERSION)"


.PHONY: upload
upload:
	python setup.py sdist
	twine upload dist/*


.PHONY: clean
clean:
	rm -rf dist/

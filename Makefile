PYTHON=python

PACKAGE = qav
VERSION = $(shell git describe --abbrev=0 --tags)
RELEASE = 1
OS_MAJOR_VERSION = $(shell lsb_release -rs | cut -f1 -d.)
OS := rhel$(OS_MAJOR_VERSION)
DIST_DIR := dist/$(OS)

CREATEREPO_WORKERS=4
YUMREPO_LOCATION=/fs/UMyumrepos/$(OS)/stable/Packages/noarch
REQUIRES := $(PYTHON),$(PYTHON)-netaddr

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
	@echo createrepo --workers=$(CREATEREPO_WORKERS) /fs/UMyumrepos/$(OS)/stable

.PHONY: build
build: rpm package

.PHONY: tag
tag:
	sed -i 's/__version__ = .*/__version__ = "$(VERSION)"/g' $(PACKAGE)/__init__.py
	git add $(PACKAGE)/__init__.py
	git commit -m "Tagging $(VERSION)"
	git tag -a $(VERSION) -m "Tagging $(VERSION)"

.PHONY: clean
clean:
	rm -rf dist/

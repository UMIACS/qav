
RPM: PYTHON = python
rhel = $(shell lsb_release -rs | cut -f1 -d.)


RPM:
ifeq ($(rhel),7)
	PYTHON=python
endif
ifeq ($(rhel),6)
	PYTHON=python
endif
ifeq ($(rhel),5)
	PYTHON=python26
endif
	$(PYTHON) setup.py bdist_rpm --requires=$(PYTHON)-netaddr

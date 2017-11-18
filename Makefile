#!/usr/bin/env make

default: pep doc test

pep:
	flake8 fpyutils/*.py tests/*.py

doc:
	$(MAKE) -C docs html

install:
	python setup.py install

test:
	python setup.py test

.PHONY: test install


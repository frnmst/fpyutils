# python-makefile
# https://software.franco.net.eu.org/frnmst/python-makefile
# MIT License
# Copyright (C) 2024 Franco Masotti (see /README.md)
PROJECT_NAME := fpyutils
PYTHON_MODULE_NAME := fpyutils

MAKEFILE_SOURCE := https://software.franco.net.eu.org/frnmst/python-makefile/raw/branch/master/Makefile
bootstrap:
	curl -o Makefile $(MAKEFILE_SOURCE)

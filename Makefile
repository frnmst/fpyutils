#!/usr/bin/env make
#
# Makefile
#
# Copyright (C) 2017-2022 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)
#
# This file is part of fpyutils.
#
# fpyutils is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# fpyutils is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with fpyutils.  If not, see <http://www.gnu.org/licenses/>.
#

export PACKAGE_NAME=fpyutils

default: doc

doc: clean
	pipenv run $(MAKE) -C docs html

install:
	pip3 install . --user

uninstall:
	pip3 uninstall --verbose --yes $(PACKAGE_NAME)

install-dev:
	pipenv install --dev
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type commit-msg
	pipenv graph
	pipenv check

uninstall-dev:
	rm -f Pipfile.lock
	pipenv --rm

update: install-dev
	pipenv run pre-commit autoupdate

test:
	pipenv run python -m unittest $(PACKAGE_NAME).tests.tests --failfast --locals --verbose

dist:
	pipenv run python setup.py sdist
	# Create a reproducible archve at least on the wheel.
	# See
	# https://bugs.python.org/issue31526
	# https://bugs.python.org/issue38727
	# https://github.com/pypa/setuptools/issues/1468
	# https://github.com/pypa/setuptools/issues/2133
	# https://reproducible-builds.org/docs/source-date-epoch/
	SOURCE_DATE_EPOCH=$$(git -c log.showSignature='false' log -1 --pretty=%ct) pipenv run python setup.py bdist_wheel
	pipenv run twine check dist/*

upload:
	pipenv run twine upload dist/*

clean:
	rm -rf build dist *.egg-info
	pipenv run $(MAKE) -C docs clean

.PHONY: default doc install uninstall install-dev uninstall-dev update test clean

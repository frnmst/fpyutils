#!/usr/bin/env make

#
# Makefile
#
# Copyright (C) 2017-2020 frnmst (Franco Masotti) <franco.masotti@live.com>
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

default: pep doc test

githook:
	git config core.hooksPath .githooks

pep:
	pipenv run yapf --style '{based_on_style: pep8; indent_width: 4; split_before_logical_operator: False}' -i fpyutils/*.py tests/*.py
	pipenv run flake8 --ignore=F401,E501,W503,W504,W605,E125,E129 fpyutils/*.py tests/*.py

doc:
	pipenv run $(MAKE) -C docs html

install:
	pip3 install . --user

uninstall:
	pip3 uninstall fpyutils

install-dev:
	pipenv install

uninstall-dev:
	pipenv --rm

test:
	pipenv run python setup.py test

dist:
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel
	pipenv run twine check dist/*

upload:
	pipenv run twine upload dist/*

clean:
	rm -rf build dist *.egg-info
	pipenv run $(MAKE) -C docs clean

.PHONY:  default pep doc install test uninstall dist upload clean

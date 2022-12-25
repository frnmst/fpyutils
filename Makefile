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

doc:
	. .venv/bin/activate \
		&& $(MAKE) -C docs html \
		&& deactivate

install:
	pip3 install . --user

uninstall:
	pip3 uninstall --verbose --yes $(PACKAGE_NAME)

install-dev:
	python3 -m venv .venv
	. .venv/bin/activate \
		&& pip install --requirement requirements.txt --requirement requirements-dev.txt \
		&& deactivate
	. .venv/bin/activate \
		&& pre-commit install \
		&& deactivate
	. .venv/bin/activate \
		&& pre-commit install --hook-type commit-msg \
		&& deactivate

uninstall-dev:
	rm -rf .venv

update: install-dev
	. .venv/bin/activate && pre-commit autoupdate \
		--repo https://github.com/pre-commit/pre-commit-hooks \
		--repo https://github.com/PyCQA/bandit \
		--repo https://github.com/pycqa/isort \
		--repo https://codeberg.org/frnmst/licheck \
		--repo https://codeberg.org/frnmst/md-toc \
		--repo https://github.com/mgedmin/check-manifest \
		--repo https://github.com/jorisroovers/gitlint \
		&& deactivate
		# --repo https://github.com/pre-commit/mirrors-mypy \

test:
	. .venv/bin/activate \
		&& python -m unittest $(PACKAGE_NAME).tests.tests --failfast --locals --verbose \
		&& deactivate

pre-commit:
	. .venv/bin/activate \
		&& pre-commit run --all \
		&& deactivate

dist:
	# Create a reproducible archive at least on the wheel.
	# See
	# https://bugs.python.org/issue31526
	# https://bugs.python.org/issue38727
	# https://github.com/pypa/setuptools/issues/1468
	# https://github.com/pypa/setuptools/issues/2133
	# https://reproducible-builds.org/docs/source-date-epoch/
	. .venv/bin/activate &&	SOURCE_DATE_EPOCH=$$(git -c log.showSignature='false' log -1 --pretty=%ct) \
		python -m build \
		&& deactivate
	. .venv/bin/activate && twine check --strict dist/* \
		&& deactivate

upload:
	pipenv run twine upload dist/*

clean:
	rm -rf build dist *.egg-info tests/benchmark-results
	# Remove all markdown files except the readmes.
	find -regex ".*\.[mM][dD]" ! -name 'README.md' ! -name 'CONTRIBUTING.md' -type f -exec rm -f {} +
	. .venv/bin/activate \
		&& $(MAKE) -C docs clean \
		&& deactivate

.PHONY: default doc install uninstall install-dev uninstall-dev update test clean demo

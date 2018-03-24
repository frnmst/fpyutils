#
# setup.py
#
# Copyright (C) 2017 frnmst (Franco Masotti) <franco.masotti@live.com>
#                                            <franco.masotti@student.unife.it>
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

from setuptools import setup, find_packages

setup(
    name='fpyutils',
    version='0.0.3',
    packages=find_packages(exclude=['*tests*']),
    license='GPL',
    description='A collection of useful non-standard Python functions which aim to be simple to use, highly readable but not efficient.',
    long_description=open('README.rst').read(),
    package_data={
        '': ['*.txt', '*.rst'],
    },
    author='Franco Masotti',
    author_email='franco.masotti@student.unife.it',
    keywords='utilities',
    url='https://github.com/frnmst/fpyutils',
    python_requires='>=3',
    # This part was inspired by:
    # https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/
    test_suite='tests',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[],
)


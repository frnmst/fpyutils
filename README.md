# fpyutils

[![PyPI fpyutils version](https://img.shields.io/pypi/v/fpyutils.svg)](https://pypi.org/project/fpyutils/)
[![Debian 12 package](https://repology.org/badge/version-for-repo/debian_12/fpyutils.svg)](https://repology.org/project/fpyutils/versions)
[![nixpkgs unstable package](https://repology.org/badge/version-for-repo/nix_unstable/python:fpyutils.svg)](https://repology.org/project/python:fpyutils/versions)
[![Anaconda.org](https://anaconda.org/conda-forge/fpyutils/badges/version.svg)](https://anaconda.org/conda-forge/fpyutils)
[![Downloads](https://pepy.tech/badge/fpyutils)](https://pepy.tech/project/fpyutils)
[![Dependent repos (via libraries.io)](https://img.shields.io/librariesio/dependent-repos/pypi/fpyutils.svg)](https://libraries.io/pypi/fpyutils/dependents)
[![Buy me a coffee](assets/buy_me_a_coffee.svg)](https://buymeacoff.ee/frnmst)

A collection of useful non-standard Python functions which aim to be
simple to use, highly readable but not efficient.

<!--TOC-->

- [fpyutils](#fpyutils)
  - [Documentation](#documentation)
  - [API examples](#api-examples)
  - [License](#license)
  - [Changelog and trusted source](#changelog-and-trusted-source)
  - [Crypto donations](#crypto-donations)

<!--TOC-->

## Documentation

<https://docs.franco.net.eu.org/fpyutils/>

## API examples

```python
>>> import fpyutils
>>> f = open('foo.txt')
>>> f.read()
"This is\nfoo.\nfoo\nThis is\nnot\nbar.\nAnd it's\n    foo\n\nBye!\n"
>>> fpyutils.filelines.get_line_matches('foo.txt','foo',5)
{1: 3, 2: 8}
```

## License

Copyright (C) 2017-2023 Franco Masotti (franco \D\o\T masotti {-A-T-} tutanota \D\o\T com)

fpyutils is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

fpyutils is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along
with fpyutils. If not, see <http://www.gnu.org/licenses/>.

## Changelog and trusted source

You can check the authenticity of new releases using my public key.

Changelogs, instructions, sources and keys can be found at
[blog.franco.net.eu.org/software/#fpyutils](https://blog.franco.net.eu.org/software/#fpyutils).

## Crypto donations

- Bitcoin: `bc1qnkflazapw3hjupawj0lm39dh9xt88s7zal5mwu`
- Monero: `84KHWDTd9hbPyGwikk33Qp5GW7o7zRwPb8kJ6u93zs4sNMpDSnM5ZTWVnUp2cudRYNT6rNqctnMQ9NbUewbj7MzCBUcrQEY`
- Dogecoin: `DMB5h2GhHiTNW7EcmDnqkYpKs6Da2wK3zP`
- Vertcoin: `vtc1qd8n3jvkd2vwrr6cpejkd9wavp4ld6xfu9hkhh0`

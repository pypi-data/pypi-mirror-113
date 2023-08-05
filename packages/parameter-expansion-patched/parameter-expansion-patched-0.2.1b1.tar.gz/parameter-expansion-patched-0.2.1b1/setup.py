# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['parameter_expansion', 'parameter_expansion.tests']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'parameter-expansion-patched',
    'version': '0.2.1b1',
    'description': 'POSIX parameter expansion in Python',
    'long_description': "# POSIX Parameter Expansion\n\n![GitHub](https://img.shields.io/github/license/kojiromike/parameter-expansion)\n![PyPI](https://img.shields.io/pypi/v/parameter-expansion)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/parameter-expansion)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/parameter-expansion)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/parameter-expansion)\n\n[![Tests](https://github.com/kojiromike/parameter-expansion/actions/workflows/test.yml/badge.svg)](https://github.com/kojiromike/parameter-expansion/actions/workflows/test.yml)\n[![CodeQL](https://github.com/kojiromike/parameter-expansion/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/kojiromike/parameter-expansion/actions/workflows/codeql-analysis.yml)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n\n\nNOTE: this is tepomrary advanced release\n\nThis is an experiment to create a Python library to enable\n[POSIX parameter expansion][1] from a string.\n\n## Obvious Test Cases\n\n```python\n    >>> from parameter_expansion import expand\n    >>> foo = 'abc/123-def.ghi'\n    >>> # Bland Expansion\n    >>> expand('abc $foo abc')\n    'abc abc/123-def.ghi abc'\n    >>> expand('abc${foo}abc')\n    'abcabc/123-def.ghiabc'\n    >>>\n    >>> # Default Value Expansion\n    >>> expand('-${foo:-bar}-')\n    '-abc/123-def.ghi-'\n    >>> expand('-${bar:-bar}-')\n    '-bar-'\n```\n\n### Default Value Expansion\n\n```python\n    >>> foo = 'abc/123-def.ghi'\n    >>> expand('abc $foo abc')\n    'abc abc/123-def.ghi abc'\n    >>> expand('abc${foo}abc')\n    'abcabc/123-def.ghiabc'\n```\n\n\n[1]: http://pubs.opengroup.org/onlinepubs/009695399/utilities/xcu_chap02.html#tag_02_06_02\n",
    'author': 'Michael A. Smith',
    'author_email': 'michael@smith-li.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

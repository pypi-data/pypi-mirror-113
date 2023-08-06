# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scipy_magic']

package_data = \
{'': ['*']}

install_requires = \
['ipython>=7.23.1,<8.0.0', 'matplotlib>=3.4.2,<4.0.0', 'scipy>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'scipy-magic',
    'version': '1.0.0',
    'description': 'SciPy Magic',
    'long_description': '[![Tests](https://github.com/tupui/scipy-magic/workflows/Tests/badge.svg?branch=master)](\nhttps://github.com/tupui/scipy-magic/actions?query=workflow%3A%22Tests%22\n)\n[![Code Quality](https://github.com/tupui/scipy-magic/workflows/Code%20Quality/badge.svg?branch=master)](\nhttps://github.com/tupui/scipy-magic/actions?query=workflow%3A%22Code+Quality%22\n)\n[![Package version](https://img.shields.io/pypi/v/scipy-magic?label=pypi%20package)](\nhttps://pypi.org/project/scipy-magic\n)\n\n# SciPy Magic: iPython extensions for SciPy\n\n## Quickstart\n\n```python\n%load_ext scipy_magic.distributions\nfrom scipy.stats import norm\nnorm(loc=3, scale=2)\n```\n![norm distribution](https://raw.githubusercontent.com/tupui/scipy-magic/main/doc/_static/norm_dist.png)\n\n## Installation\n\nThe latest stable release (and older versions) can be installed from PyPI:\n\n    pip install scipy-magic\n\nYou may instead want to use the development version from Github. Poetry is\nneeded and can be installed either from PyPI or:\n\n    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python\n\nThen once you cloned the repository, you can install it with:\n\n    poetry install\n\n## Contributing\n\nWant to add a cool logo, more doc, tests or new features? Contributors are more\nthan welcome! Feel free to open an [issue](https://github.com/tupui/scipy-magic/issues)\nor even better propose changes with a [PR](https://github.com/tupui/scipy-magic/compare).\nHave a look at the contributing guide.\n',
    'author': 'Pamphile Roy',
    'author_email': 'roy.pamphile@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tupui/scipy-magic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)

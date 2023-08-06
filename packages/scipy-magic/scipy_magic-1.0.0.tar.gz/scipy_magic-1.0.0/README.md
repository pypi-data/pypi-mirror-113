[![Tests](https://github.com/tupui/scipy-magic/workflows/Tests/badge.svg?branch=master)](
https://github.com/tupui/scipy-magic/actions?query=workflow%3A%22Tests%22
)
[![Code Quality](https://github.com/tupui/scipy-magic/workflows/Code%20Quality/badge.svg?branch=master)](
https://github.com/tupui/scipy-magic/actions?query=workflow%3A%22Code+Quality%22
)
[![Package version](https://img.shields.io/pypi/v/scipy-magic?label=pypi%20package)](
https://pypi.org/project/scipy-magic
)

# SciPy Magic: iPython extensions for SciPy

## Quickstart

```python
%load_ext scipy_magic.distributions
from scipy.stats import norm
norm(loc=3, scale=2)
```
![norm distribution](https://raw.githubusercontent.com/tupui/scipy-magic/main/doc/_static/norm_dist.png)

## Installation

The latest stable release (and older versions) can be installed from PyPI:

    pip install scipy-magic

You may instead want to use the development version from Github. Poetry is
needed and can be installed either from PyPI or:

    curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

Then once you cloned the repository, you can install it with:

    poetry install

## Contributing

Want to add a cool logo, more doc, tests or new features? Contributors are more
than welcome! Feel free to open an [issue](https://github.com/tupui/scipy-magic/issues)
or even better propose changes with a [PR](https://github.com/tupui/scipy-magic/compare).
Have a look at the contributing guide.

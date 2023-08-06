# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_integration_mark']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=5.2,<7.0']

entry_points = \
{'pytest11': ['pytest_integration_mark = pytest_integration_mark.hooks']}

setup_kwargs = {
    'name': 'pytest-integration-mark',
    'version': '0.1.0',
    'description': 'Automatic integration test marking and excluding plugin for pytest',
    'long_description': '[![Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI version](https://badge.fury.io/py/pytest-integration-mark.svg)](https://pypi.org/project/pytest-integration-mark/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytest-integration-mark)](https://pypi.org/project/pytest-integration-mark/)\n\n\n# Description\nProvides a pytest marker `integration` for integration tests. \nThis marker automatically applies to all tests in a specified integration test folder.\nIntegration tests will not run by default, which is useful for cases where an external dependency\nneeds to be set up first (such as a database service).\n\n# Installation\n\nThis is a pure python package, so it can be installed with `pip install pytest-integration-mark` \nor any other dependency manager.\n\n# Usage\n\nAfter installation:\n\nRunning `pytest` as usual:\n- Tests marked with `@pytest.mark.integration` will be skipped\n- Tests in `./tests/integration/...` will be skipped\n\nRunning `pytest --with-integration`:\n- Tests marked with `@pytest.mark.integration` will run\n- Tests in `./tests/integration/...` will run\n\nRunning `pytest --with-integration --integration-tests-folder integration`:\n- Tests marked with `@pytest.mark.integration` will run\n- Tests in `./integration/...` will run\n\n# Development\n\nThis library uses the [poetry](https://python-poetry.org/) package manager, which has to be installed before installing\nother dependencies. Afterwards, run `poetry install` to create a virtualenv and install all dependencies.\nTo then activate that environment, use `poetry shell`. To run a command in the environment without activating it,\nuse `poetry run <command>`.\n\n[Black](https://github.com/psf/black) is used (and enforced via workflows) to format all code. Poetry will install it\nautomatically, but running it is up to the user. To format the entire project, run `black .` inside the virtualenv.\n\n# Contributing\n\nThis project uses the Apache 2.0 license and is maintained by the data science team @ Barbora. All contribution are \nwelcome in the form of PRs or raised issues.\n',
    'author': 'Saulius Beinorius',
    'author_email': 'saulius.beinorius@gmail.com',
    'maintainer': 'Saulius Beinorius',
    'maintainer_email': 'saulius.beinorius@gmail.com',
    'url': 'https://github.com/Barbora-Data-Science/pytest-integration-mark',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

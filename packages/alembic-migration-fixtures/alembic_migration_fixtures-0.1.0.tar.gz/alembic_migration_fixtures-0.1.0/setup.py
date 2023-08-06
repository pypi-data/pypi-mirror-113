# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alembic_migration_fixtures']

package_data = \
{'': ['*']}

install_requires = \
['SQLAlchemy>=1.3.19,<1.5', 'alembic>=1.4.2,<1.7', 'pytest>=5.2,<7.0']

entry_points = \
{'pytest11': ['alembic_migration_fixtures = '
              'alembic_migration_fixtures.fixtures']}

setup_kwargs = {
    'name': 'alembic-migration-fixtures',
    'version': '0.1.0',
    'description': 'Pytest fixtures for tests involving databases managed by alembic migrations',
    'long_description': '[![Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![PyPI version](https://badge.fury.io/py/alembic-migration-fixtures.svg)](https://pypi.org/project/alembic-migration-fixtures/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/alembic-migration-fixtures)](https://pypi.org/project/alembic-migration-fixtures/)\n\n\n# Description\nPytest fixture to simplify writing tests against databases managed with `alembic`.\nBefore each test run, alembic migrations apply schema changes which then allows tests to only care about data.\nThis way your application code, and the database migrations get executed by the test.\n\nOnly tested with PosgreSQL. However, code may work with other databases as well.\n\n# Installation\n\nInstall with `pip install alembic-migration-fixtures` or any other dependency manager.\nAfterwards, create a pytest fixture called `database_engine` returning an SQLAlchemy `Engine` instance.\n\n_WARNING_\n\nDo not specify the production / development / any other database where data is important in the engine fixture.\nIf you do so, the tests WILL truncate all tables and data loss WILL occur.\n\n\n# Usage\n\nThis library provides a pytest [fixture](https://docs.pytest.org/en/6.2.x/fixture.html) called `test_db_session`.\nUse this to replace the normal SQLAlchemy session used within the application, or else tests may not be independent \nof one another. \n\nHow the fixture works with your tests:\n1. Fixture recreates (wipes) the database schema based on the engine provided for the test session\n1. Fixture runs alembic migrations (equivalent to `alembic upgrade heads`)\n1. Fixture creates a test database session within a transaction for the test\n1. Your test sets up data and runs the test using the session (including `COMMIT`ing transactions)\n1. Your test verifies data is in the database\n1. Fixture rolls back the transaction (and any inner `COMMIT`ed transactions in the test)\n\nThis two-level transaction strategy makes it so any test is independent of one another, \nsince the database is empty after each test. Since the database schema only gets re-created once per session,\nthe test speed is only linearly dependent on the number of migrations.\n\n\n# Development\n\nThis library uses the [poetry](https://python-poetry.org/) package manager, which has to be installed before installing\nother dependencies. Afterwards, run `poetry install` to create a virtualenv and install all dependencies.\nTo then activate that environment, use `poetry shell`. To run a command in the environment without activating it,\nuse `poetry run <command>`.\n\n[Black](https://github.com/psf/black) is used (and enforced via workflows) to format all code. Poetry will install it\nautomatically, but running it is up to the user. To format the entire project, run `black .` inside the virtualenv.\n\n# Contributing\n\nThis project uses the Apache 2.0 license and is maintained by the data science team @ Barbora. All contribution are \nwelcome in the form of PRs or raised issues.\n',
    'author': 'Saulius Beinorius',
    'author_email': 'saulius.beinorius@gmail.com',
    'maintainer': 'Saulius Beinorius',
    'maintainer_email': 'saulius.beinorius@gmail.com',
    'url': 'https://github.com/Barbora-Data-Science/alembic-migration-fixtures',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

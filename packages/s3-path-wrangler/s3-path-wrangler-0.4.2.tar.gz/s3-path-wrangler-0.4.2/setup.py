# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_path_wrangler']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 's3-path-wrangler',
    'version': '0.4.2',
    'description': 'Provides S3 path manipulation, similar to PurePath in pathlib',
    'long_description': '[![License](https://img.shields.io/hexpm/l/s3-path-wrangler)](LICENSE)\n[![Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Build Status](https://github.com/Barbora-Data-Science/s3-path-wrangler/actions/workflows/main.yml/badge.svg)](https://github.com/Barbora-Data-Science/s3-path-wrangler/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/Barbora-Data-Science/s3-path-wrangler/branch/main/graph/badge.svg?token=MJSSVCSFJV)](https://codecov.io/gh/Barbora-Data-Science/s3-path-wrangler)\n[![PyPI version](https://badge.fury.io/py/s3-path-wrangler.svg)](https://pypi.org/project/s3-path-wrangler/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/s3-path-wrangler)](https://pypi.org/project/s3-path-wrangler/)\n\n\n# Description\nProvides S3 path manipulation, similar to PurePath in pathlib. \nS3Path is _only_ meant for path manipulation and does not implement any methods which interact with S3 itself.\nAvoiding S3 interaction means that a user can use their own boto3 session and are not forced to use the default one.\n\nFor S3Path implementations that do path manipulation _and_ interaction, see \n[s3path](https://github.com/liormizr/s3path) instead.\n\n# Installation\n\nThis is a pure python package, so it can be installed with `pip install s3-path-wrangler` \nor any other dependency manager.\n\n# Usage\n\nThis library provides a single (meant to be) immutable class - `S3Path`.\nClass features:\n\n```python\nfrom s3_path_wrangler.paths import S3Path\n\n# various options for creating path objects\nfull_path = S3Path("s3://your-bucket/some/path/file.json")\nfrom_list = S3Path.from_parts(["your-bucket", "some", "path", "file.json"], is_absolute=True)\nrelative = S3Path("some/path/")\nrelative_from_list = S3Path.from_parts(["some", "path"]) # or is_absolute=False\n\n# convenient attributes\nassert full_path.parts == ["your-bucket", "some", "path", "file.json"]\nassert full_path.is_absolute == True\nassert full_path.bucket == "your-bucket"\nassert full_path.key == "some/path/file.json"\nassert full_path.name == "file.json"\nassert full_path.parent == S3Path("s3://your-bucket/some/path")\n\n# paths are comparable to strings (directories will not have trailing slashes)\nassert S3Path.from_parts(["some", "path"]) == "some/path"\n\n# paths can be manipulated via \'/\'\nassert relative / "file.json" == S3Path("some/path/file.json")\n```\n\n# Development\n\nThis library uses the [poetry](https://python-poetry.org/) package manager, which has to be installed before installing\nother dependencies. Afterwards, run `poetry install` to create a virtualenv and install all dependencies.\n\n[Black](https://github.com/psf/black) is used (and enforced via workflows) to format all code. Poetry will install it\nautomatically, but running it is up to the user. To format the entire project, run `black .`.\n\nTo run tests, either activate the virtualenv via `poetry shell` and run `pytest ./tests`,\nor simply run `poetry run pytest ./tests`.\n\n# Contributing\n\nThis project uses the Apache 2.0 license and is maintained by the data science team @ Barbora. All contribution are \nwelcome in the form of PRs or raised issues.\n',
    'author': 'Saulius Beinorius',
    'author_email': 'saulius.beinorius@gmail.com',
    'maintainer': 'Saulius Beinorius',
    'maintainer_email': 'saulius.beinorius@gmail.com',
    'url': 'https://github.com/Barbora-Data-Science/s3-path-wrangler',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

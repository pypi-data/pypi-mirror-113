# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['drf_rw_serializers-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'drf-rw-serializers-stubs',
    'version': '1.0.4',
    'description': 'Type stubs for the drf-rw-serializers package',
    'long_description': '# drf-rw-serializers-stubs\n\n[![PyPI](https://img.shields.io/pypi/v/drf-rw-serializers-stubs)](https://pypi.org/project/drf-rw-serializers-stubs/)\n\nPython type stubs for the [drf-rw-serializers](https://github.com/vintasoftware/drf-rw-serializers) package.\n\n## Usage\n\n```\npip install drf-rw-serializers-stubs\n```\n',
    'author': 'Nikhil Benesch',
    'author_email': 'nikhil.benesch@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/benesch/drf-rw-serializers-stubs',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

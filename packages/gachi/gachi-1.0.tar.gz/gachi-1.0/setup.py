# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gachi']

package_data = \
{'': ['*'], 'gachi': ['data/*']}

setup_kwargs = {
    'name': 'gachi',
    'version': '1.0',
    'description': 'No description',
    'long_description': None,
    'author': 'Anonymous',
    'author_email': 'anal@gadgets.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

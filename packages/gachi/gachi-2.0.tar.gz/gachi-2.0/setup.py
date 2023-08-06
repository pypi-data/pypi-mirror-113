# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gachi']

package_data = \
{'': ['*'], 'gachi': ['data/*']}

install_requires = \
['pyglet>=1.5.18,<2.0.0']

setup_kwargs = {
    'name': 'gachi',
    'version': '2.0',
    'description': 'No description',
    'long_description': None,
    'author': 'Anonymous',
    'author_email': 'anal@gadgets.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

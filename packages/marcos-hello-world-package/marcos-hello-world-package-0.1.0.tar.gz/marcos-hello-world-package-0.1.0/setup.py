# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marcos_hello_world_package']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'marcos-hello-world-package',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Marco Gancitano',
    'author_email': 'marco.gancitano97@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

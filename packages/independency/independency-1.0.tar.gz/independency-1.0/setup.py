# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['independency']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'independency',
    'version': '1.0',
    'description': '',
    'long_description': None,
    'author': 'apollon',
    'author_email': 'Apollon76@yandex.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

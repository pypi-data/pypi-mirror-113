# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ninja_auth']

package_data = \
{'': ['*']}

install_requires = \
['django-ninja>=0.13.2,<0.14.0']

setup_kwargs = {
    'name': 'django-ninja-auth',
    'version': '0.1.0',
    'description': 'Django authorization views adapted to django-ninja',
    'long_description': None,
    'author': 'Martín Ugarte',
    'author_email': 'contact@martinugarte.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

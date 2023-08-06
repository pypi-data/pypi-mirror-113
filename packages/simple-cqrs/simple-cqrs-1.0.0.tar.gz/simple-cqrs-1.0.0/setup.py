# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_cqrs', 'simple_cqrs.cqrs', 'simple_cqrs.helpers']

package_data = \
{'': ['*']}

install_requires = \
['funcy>=1.14,<2.0',
 'marshmallow>=3.3.0,<4.0.0',
 'methoddispatch>=3.0.2,<4.0.0',
 'pytz>=2019.3,<2020.0',
 'singleton-py3>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'simple-cqrs',
    'version': '1.0.0',
    'description': 'CQRS and Event Sourcing made simple',
    'long_description': None,
    'author': 'David Jiménez (Rydra)',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)

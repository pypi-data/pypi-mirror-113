# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['google_analytics_client']

package_data = \
{'': ['*']}

install_requires = \
['google-api-python-client>=2.13.0,<3.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'pandas>=1.3.0,<2.0.0']

setup_kwargs = {
    'name': 'google-analytics-client',
    'version': '0.1.2',
    'description': 'Google Analytics client for Python3',
    'long_description': None,
    'author': 'Mikhail Vasilchenko',
    'author_email': 'rekoy88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

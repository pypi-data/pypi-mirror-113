# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tradernet_client']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'tradernet-client',
    'version': '0.6.0',
    'description': '',
    'long_description': None,
    'author': 'roci',
    'author_email': 'rocinantt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

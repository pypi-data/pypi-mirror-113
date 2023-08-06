# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pystructopt']

package_data = \
{'': ['*']}

install_requires = \
['dataclass-utils>=0.7.14,<1', 'typing-extensions>=3.10.0,<4.0.0']

setup_kwargs = {
    'name': 'pystructopt',
    'version': '0.1.6',
    'description': '',
    'long_description': None,
    'author': 'Yohei Tamura',
    'author_email': 'tamuhey@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

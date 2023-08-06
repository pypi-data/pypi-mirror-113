# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_orm']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-orm',
    'version': '0.1.0',
    'description': 'An asynchronous ORM that uses pydantic.',
    'long_description': None,
    'author': 'Ronald Williams',
    'author_email': 'ronaldnwilliams@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

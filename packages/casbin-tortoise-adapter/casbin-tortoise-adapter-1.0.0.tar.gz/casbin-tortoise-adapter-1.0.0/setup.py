# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casbin_tortoise_adapter']

package_data = \
{'': ['*']}

install_requires = \
['asynccasbin>=1.1.2,<2.0.0', 'tortoise-orm>=0.16.6']

extras_require = \
{'linting': ['black>=21.7b0,<22.0',
             'flake8>=3.9.2,<4.0.0',
             'isort>=5.9.2,<6.0.0',
             'mypy>=0.910,<0.911']}

setup_kwargs = {
    'name': 'casbin-tortoise-adapter',
    'version': '1.0.0',
    'description': 'Tortoise ORM for AsyncCasbin',
    'long_description': None,
    'author': 'Elias Gabriel',
    'author_email': 'me@eliasfgabriel.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

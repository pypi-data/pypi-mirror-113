# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['marsworks', 'marsworks.origin']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'marsworks',
    'version': '0.2.1',
    'description': "An Async. API Wrapper around NASA's Mars Photos API written in Python.",
    'long_description': None,
    'author': 'NovaEmiya',
    'author_email': 'importz750@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

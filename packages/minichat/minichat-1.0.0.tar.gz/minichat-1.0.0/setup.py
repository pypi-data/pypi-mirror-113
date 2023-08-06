# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['minichat']

package_data = \
{'': ['*'], 'minichat': ['aiml_data/alice/*', 'aiml_data/custom/*']}

install_requires = \
['python-aiml==0.9.3']

setup_kwargs = {
    'name': 'minichat',
    'version': '1.0.0',
    'description': 'Mini chatbot client based on AIML',
    'long_description': None,
    'author': 'DevAndromeda',
    'author_email': 'devandromeda@snowflakedev.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matrix_webhook']

package_data = \
{'': ['*']}

install_requires = \
['Markdown>=3.3.4,<4.0.0', 'matrix-nio>=0.18.3,<0.19.0']

setup_kwargs = {
    'name': 'matrix-webhook',
    'version': '3.0.0',
    'description': 'Post a message to a matrix room with a simple HTTP POST',
    'long_description': None,
    'author': 'Guilhem Saurel',
    'author_email': 'guilhem.saurel@laas.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

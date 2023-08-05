# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['darbiadev_sanmar', 'darbiadev_sanmar.lib']

package_data = \
{'': ['*']}

install_requires = \
['python-benedict>=0.24.0,<0.25.0',
 'suds-community>=0.8.5,<0.9.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'darbiadev-sanmar',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Bradley Reynolds',
    'author_email': 'bradley.reynolds@darbia.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

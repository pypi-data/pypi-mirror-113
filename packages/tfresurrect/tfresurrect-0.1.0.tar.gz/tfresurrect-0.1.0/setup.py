# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tfresurrect']

package_data = \
{'': ['*']}

install_requires = \
['c7n>=0.9.11,<0.10.0', 'python-hcl2>=2.0.3,<3.0.0']

entry_points = \
{'console_scripts': ['tfresurrect = tfresurrect.cli:cli']}

setup_kwargs = {
    'name': 'tfresurrect',
    'version': '0.1.0',
    'description': 'resurrect terraform state',
    'long_description': None,
    'author': 'Kapil Thangavelu',
    'author_email': 'hello@stacklet.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

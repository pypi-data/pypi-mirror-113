# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carbonify']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.4.2,<4.0.0',
 'nltk>=3.6.2,<4.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.3.0,<2.0.0',
 'plotly>=5.1.0,<6.0.0',
 'streamlit>=0.84.1,<0.85.0',
 'tqdm>=4.61.2,<5.0.0']

setup_kwargs = {
    'name': 'carbonify',
    'version': '0.1.0',
    'description': 'Open source library for carbon accounting and Lifecycle analysis',
    'long_description': None,
    'author': 'Theo Alves Da Costa',
    'author_email': 'theo.alvesdacosta@ekimetrics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

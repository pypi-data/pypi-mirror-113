# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kiez',
 'kiez.analysis',
 'kiez.evaluate',
 'kiez.hubness_reduction',
 'kiez.io',
 'kiez.neighbors',
 'kiez.neighbors.approximate',
 'kiez.neighbors.exact',
 'kiez.utils']

package_data = \
{'': ['*']}

install_requires = \
['annoy>=1.17.0,<2.0.0',
 'importlib-metadata',
 'joblib>=1.0.0,<2.0.0',
 'ngt>=1.12.2,<2.0.0',
 'nmslib>=2.1.1,<3.0.0',
 'numpy>=1.20.0,<2.0.0',
 'pandas>=1.2.1,<2.0.0',
 'scikit-learn>=0.24.1,<0.25.0',
 'scipy>=1.6.0,<2.0.0',
 'tqdm>=4.56.0,<5.0.0']

setup_kwargs = {
    'name': 'kiez',
    'version': '0.2.0',
    'description': 'Hubness reduced nearest neighbor search for entity alignment with knowledge graph embeddings',
    'long_description': None,
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

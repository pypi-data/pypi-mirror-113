# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['chemical_calculators']
install_requires = \
['numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'chemical-calculators',
    'version': '0.0.3',
    'description': 'Various calculators for chemistry',
    'long_description': None,
    'author': 'Yakovlev Kll',
    'author_email': 'yakovlev.kll@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

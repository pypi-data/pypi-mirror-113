# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['chemical_calculators',
 'chemical_calculators.core',
 'chemical_calculators.helpers',
 'chemical_calculators.ui',
 'chemical_calculators.ui.tkinter',
 'chemical_calculators.ui.tkinter.modules']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.0,<2.0.0']

setup_kwargs = {
    'name': 'chemical-calculators',
    'version': '0.0.2',
    'description': 'Various calculators for chemistry',
    'long_description': None,
    'author': 'Yakovlev Kll',
    'author_email': 'yakovlev.kll@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

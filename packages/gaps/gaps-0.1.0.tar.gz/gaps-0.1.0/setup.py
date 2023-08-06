# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gaps']

package_data = \
{'': ['*']}

install_requires = \
['frozendict>=2.0.3,<3.0.0']

setup_kwargs = {
    'name': 'gaps',
    'version': '0.1.0',
    'description': 'Generalized assignment problem solver',
    'long_description': '# GAPS\n\n_Generalized Assignment Problem Solver_\n\nThis code aims to implement an efficient solver for the generalized assignment problem.\n',
    'author': 'Stijn de Gooijer',
    'author_email': 'stijn@degooijer.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stinodego/gaps',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

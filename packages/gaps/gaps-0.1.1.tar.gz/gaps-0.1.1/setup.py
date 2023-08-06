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
    'version': '0.1.1',
    'description': 'Generalized assignment problem solver',
    'long_description': "# GAPS\n\n_Generalized Assignment Problem Solver_\n\nThis code aims to implement an efficient solver for the generalized assignment problem.\n\n## The generalized assignment problem\n\nThe generalized assignment problem is described quite well [on Wikipedia](https://en.wikipedia.org/wiki/Generalized_assignment_problem).\n\nThis code actually allows for further generalization, multiple agents to perform a single task (regulated by a task budget).\n\n## The implementation\n\nThe implementation is a simple depth-first search algorithm. Therefore, it does not work well for very large problems.\n\nThe depth-first search expands most promising nodes first. True maximum assignment is guaranteed when algorithm is allowed to complete. Otherwise, the assignment printed last may be used as a best guess.\n\nThe code makes use of `frozendict` to keep track of the set of assignments.\n\n## Running the code\n\nSolving your assignment problem is easy. Just specify your assignment problem (refer to main method in `assign.py` for an example), then run it. An example problem specification is given, to make clear what syntax is expected.\n\nThe code offers a few features:\n* Optional 'hard assignment' initializes the assignment with certain agents assigned to certain tasks\n* Optional 'fair' parameter maximizes the profits related to the least profitable task (and thus equalizes the profits among tasks).\n* Optional 'complete' parameter requires agents and tasks to fully use their budgets.\n* 'verbose' option prettily prints the assignment information after the code finishes. May be turned off.\n",
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

# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hall']

package_data = \
{'': ['*']}

install_requires = \
['mpmath>=1.2,<2.0']

entry_points = \
{'console_scripts': ['docs = scripts.poetry:docs',
                     'reformat = scripts.poetry:reformat',
                     'test = scripts.poetry:test']}

setup_kwargs = {
    'name': 'hall',
    'version': '0.1.3',
    'description': 'Hall - Probability theory using pythonic and (almost) mathematical notation.',
    'long_description': 'Probability theory using pythonic and (almost) mathematical notation.\n\n## Help\n\nSee [documentation](https://jorenham.github.io/hall/) for more details.\n\n## A simple example: Intelligence quotient\n\n```pycon\n>>> from hall import P, E, Std, Normal\n>>> IQ = ~Normal(100, 15)\n>>> E[IQ]\n100.0\n>>> Std[IQ]\n15.0\n>>> P(X >= 130)\n0.0227501319481792\n```\n\nSo the chance of having an IQ (normally distributed with μ=100 and σ=15) of at \nleast 130 is approximately 2.3%.\n\n## A simple example: Monty ~~Python~~ Hall \n\n`TODO`\n\n## Contributing\n\nFor guidance on setting up a development environment and how to make a\ncontribution to *hall*, see\n[Contributing to Pydantic](https://jorenham.github.io/hall/#contributing).',
    'author': 'Joren Hammudoglu',
    'author_email': 'jhammudoglu@gmail.com',
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

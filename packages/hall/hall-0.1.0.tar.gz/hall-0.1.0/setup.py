# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hall']

package_data = \
{'': ['*']}

install_requires = \
['mpmath>=1.2,<2.0']

setup_kwargs = {
    'name': 'hall',
    'version': '0.1.0',
    'description': 'Hall - Probability theory using pythonic and (almost) mathematical notation.',
    'long_description': '# Hall\n\nProbability theory using pythonic and (almost) mathematical notation.\n\n## A simple example: Monty ~~Python~~ Hall \n\n`TODO`\n\n## Contributing\n\nEnsure you have [poetry](https://python-poetry.org/docs/#installation) installed, then\n\n```bash\npoetry install\n```\n',
    'author': 'Joren Hammudoglu',
    'author_email': 'jhammudoglu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

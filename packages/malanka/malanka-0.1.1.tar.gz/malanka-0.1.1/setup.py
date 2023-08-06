# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malanka']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'malanka',
    'version': '0.1.1',
    'description': 'WebSocket channels.',
    'long_description': '## WebSocket channels for ASGI\n\n\n## Installation\n\nInstall `malanka` using PIP or poetry:\n\n```bash\npip install malanka\n# or\npoetry add malanka\n```\n\n## Quick start\n\nSee example application in `examples/` directory of this repository.\n',
    'author': 'alex.oleshkevich',
    'author_email': 'alex.oleshkevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alex-oleshkevich/malanka',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

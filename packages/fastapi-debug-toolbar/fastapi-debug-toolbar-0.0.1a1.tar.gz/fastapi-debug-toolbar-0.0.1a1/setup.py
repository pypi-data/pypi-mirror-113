# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['debug_toolbar', 'debug_toolbar.panels']

package_data = \
{'': ['*'],
 'debug_toolbar': ['statics/css/*',
                   'statics/js/*',
                   'templates/*',
                   'templates/includes/*',
                   'templates/panels/*']}

install_requires = \
['Jinja2>=2.9,<3.0', 'fastapi>=0.51.0,<0.52.0', 'pyinstrument>=3.0.0,<4.0.0']

setup_kwargs = {
    'name': 'fastapi-debug-toolbar',
    'version': '0.0.1a1',
    'description': 'A debug toolbar for FastAPI.',
    'long_description': '# FastAPI Debug Toolbar\n\nA debug toolbar for FastAPI based on the original django-debug-toolbar.\n\n## Installation\n\n```shell\npip install fastapi-debug-toolbar\n```\n\n## Quickstart\n\n```py\nfrom fastapi import FastAPI\nfrom debug_toolbar.middleware import DebugToolbarMiddleware\n\napp = FastAPI(debug=True)\napp.add_middleware(DebugToolbarMiddleware)\n```\n',
    'author': 'Dani',
    'author_email': 'dani@domake.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mongkok/fastapi-debug-toolbar',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

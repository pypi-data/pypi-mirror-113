# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linkedin_matrix',
 'linkedin_matrix.commands',
 'linkedin_matrix.db',
 'linkedin_matrix.db.upgrade',
 'linkedin_matrix.formatter',
 'linkedin_matrix.web']

package_data = \
{'': ['*']}

install_requires = \
['asyncpg>=0.22.0,<0.23.0',
 'commonmark>=0.9.1,<0.10.0',
 'linkedin-messaging>=0.2.1,<0.3.0',
 'mautrix>=0.9.8,<0.10.0',
 'python-magic>=0.4.24,<0.5.0',
 'ruamel.yaml>=0.17.10,<0.18.0']

extras_require = \
{'e2be': ['python-olm==3.2.1', 'unpaddedbase64>=2.1.0,<3.0.0'],
 'images': ['Pillow>=8.3.0,<9.0.0']}

setup_kwargs = {
    'name': 'linkedin-matrix',
    'version': '0.2.0',
    'description': 'A Matrix-LinkedIn Messages puppeting bridge.',
    'long_description': '# linkedin-matrix\n\n[![pipeline status](https://gitlab.com/beeper/linkedin-matrix/badges/master/pipeline.svg)](https://gitlab.com/beeper/linkedin-matrix/-/commits/master) \n[![Matrix Chat](https://img.shields.io/matrix/linkedin-matrix:nevarro.space?server_fqdn=matrix.nevarro.space)](https://matrix.to/#/#linkedin-matrix:nevarro.space?via=nevarro.space&via=sumnerevans.com)\n[![Apache 2.0](https://img.shields.io/github/license/sumnerevans/linkedin-matrix)](https://github.com/sumnerevans/linkedin-matrix/blob/master/LICENSE)\n\nLinkedIn Messaging <-> Matrix bridge built using\n[mautrix-python](https://github.com/tulir/mautrix-python) and\n[linkedin-messaging-api](https://github.com/sumnerevans/linkedin-messaging-api).\n\n## Documentation\n\nNot any yet :)\n\n### Features & Roadmap\n[ROADMAP.md](https://github.com/sumnerevans/linkedin-matrix/blob/master/ROADMAP.md)\ncontains a general overview of what is supported by the bridge.\n\n## Discussion\n\nMatrix room:\n[`#linkedin-matrix:nevarro.space`](https://matrix.to/#/#linkedin-matrix:nevarro.space?via=nevarro.space&via=sumnerevans.com)\n',
    'author': 'Sumner Evans',
    'author_email': 'inquiries@sumnerevans.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sumnerevans/linkedin-matrix',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

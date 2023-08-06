# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['emoji_shortname']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=4.1.0,<5.0.0', 'emoji>=1.2.0,<2.0.0']

extras_require = \
{':python_version >= "3.7" and python_version < "3.8"': ['importlib-metadata>=4.6.1,<5.0.0']}

setup_kwargs = {
    'name': 'emoji-shortname',
    'version': '0.1.0',
    'description': 'Replace emoji short names with their corresponding emojis.',
    'long_description': None,
    'author': 'Nick Phair',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

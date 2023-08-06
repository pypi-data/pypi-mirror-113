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
    'version': '0.1.1',
    'description': 'Replace emoji short names with their corresponding emojis.',
    'long_description': '[![Build Status](https://github.com/nicholasphair/emoji-shortname/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/nicholasphair/emoji-shortname/actions/workflows/build.yml)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)\n\n\n# emoji-shortname\nReplace emoji short names with their corresponding emojis.\n\n## Overview\nThe short names we are familiar with (e.g. the ones used on sites like GitHub)\nare not inline with the [CLDR short names][1] defined in the Unicode standard.\nThis makes mapping short codes to emojis a bit of a challenge. So, I punt on\nthis issue, and defer to the [emoji package][2] created by [Taehoon Kim and Kevin Wurster][3].\nTheir wonderful library does the heavy lifting.  \n\nThis extension amounts to a find-and-replace. Find the short name, replace it with the\nappropriate emoji. It works with both `Markdown` and `reStructuredText`.\n\n## Details\nEmojis are added to documents by sandwiching their short names between colons.\nFor example, `:smile:` resolves to :smile:. This syntax conflicts with\nthe way you provide options to directives in Sphinx. And, since the extension\nties into the [source-read hook][4], those directives are yet to be resolved.\nAs such, if an option shares the same name as an emoji short code, the option\nwill be replaced by the emoji. Though I am unaware of any case where this happens,\nbe aware that it is a possibility.\n\n## Development\nThe project is managed with [poetry][5].  \n\nTo contribute to `emoji-shortname`, first [install poetry][6]. Once installed,\nfetch the project dependencies with `poetry install`. From here, you can\niterate on the code and run the unit tests with `poetry run tox pyproject.toml`\n\n## Usage\nSimply install the package with your manager of choice (e.g. poetry, pip, etc)\nand then add the extension to your sphinx `config.py`.\n```python\nextensions = ["emoji_shortname"]\n```\n\n[1]: https://unicode.org/emoji/charts/full-emoji-list.html\n[2]: https://github.com/carpedm20/emoji/\n[3]: https://github.com/carpedm20/emoji/blob/master/LICENSE.txt\n[4]: https://www.sphinx-doc.org/en/master/extdev/appapi.html#event-source-read\n[5]: https://python-poetry.org/\n[6]: https://python-poetry.org/docs/#installation\n',
    'author': 'Nick Phair',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nicholasphair/emoji-shortname',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)

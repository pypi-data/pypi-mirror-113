# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['batch_tr']

package_data = \
{'': ['*']}

install_requires = \
['logzero>=1.7.0,<2.0.0', 'translatepy>=1.7,<2.0']

setup_kwargs = {
    'name': 'batch-tr',
    'version': '0.1.0',
    'description': 'batch machine translate via pythonpy',
    'long_description': '# batch_tr\n<!--- batch-tr  batch_tr  batch_tr batch_tr --->\n[![tests](https://github.com/ffreemt/batch-tr/actions/workflows/routine-tests.yml/badge.svg)][![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/batch_tr.svg)](https://badge.fury.io/py/batch_tr)\n\nbatch translate long text and list of texts at 10000 chars/s\n\n<!-- snippets-mat\\deepl-translate-memo.txt -->\n\n## Use It\n\n```python\nfrom batch_tr.batch_tr import batch_tr\n\nres = batch_tr("very long text " * 10000)\nprint(res)\n# to chinese/zh\n\nprint(batch_tr("test me", to_lang="de"))\n\n# long list\nres = batch_tr(("very long text \\n" * 10000).splitlines())\n# equally long list of translated text\n# known to work for to_lang="zh" (default)\nprint(res)\n```',
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/batch-tr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.7,<4.0.0',
}


setup(**setup_kwargs)

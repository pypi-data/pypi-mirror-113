# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xarray_quantity']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=4.2.1,<5.0.0', 'xarray>=0.18.2,<0.19.0']

setup_kwargs = {
    'name': 'xarray-quantity',
    'version': '0.1.0',
    'description': 'xarray extension which supports astropy quantities.',
    'long_description': '# python-template\n\n[![PyPI](https://img.shields.io/pypi/v/PACKAGENAME.svg?label=PyPI&style=flat-square)](https://pypi.org/pypi/PACKAGENAME/)\n[![Python](https://img.shields.io/pypi/pyversions/PACKAGENAME.svg?label=Python&color=yellow&style=flat-square)](https://pypi.org/pypi/PACKAGENAME/)\n[![Test](https://img.shields.io/github/workflow/status/USERNAME/PACKAGENAME/Test?logo=github&label=Test&style=flat-square)](https://github.com/USERNAME/PACKAGENAME/actions)\n[![License](https://img.shields.io/badge/license-MIT-blue.svg?label=License&style=flat-square)](LICENSE)\n\nPython package template.\n\n## Features\n\nThis library provides:\n\n- something.\n\n## Installation\n\n```shell\npip install PACKAGENAME\n```\n\n## Usage\n\n### 1st module\n\n### 2nd module\n\n---\n\nThis library is using [Semantic Versioning](https://semver.org).\n',
    'author': 'KaoruNishikawa',
    'author_email': 'k.nishikawa@a.phys.nagoya-u.ac.jp',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/KaoruNishikawa/xarray-quantity',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

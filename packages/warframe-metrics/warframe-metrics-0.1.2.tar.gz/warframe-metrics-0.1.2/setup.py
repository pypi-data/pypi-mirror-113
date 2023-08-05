# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['warframe_metrics',
 'warframe_metrics.analysis',
 'warframe_metrics.market',
 'warframe_metrics.utils']

package_data = \
{'': ['*']}

install_requires = \
['alive-progress>=1.6.2,<2.0.0',
 'desert>=2020.11.18,<2021.0.0',
 'pandas>=1.2.4,<2.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'warframe-metrics',
    'version': '0.1.2',
    'description': 'Warframe market metrics package.',
    'long_description': '<p align="center"><a href="https://raw.githubusercontent.com/rajivsarvepalli/warframe-metrics/main/docs/_static/warframe_logo.jpg"><img src="https://raw.githubusercontent.com/rajivsarvepalli/warframe-metrics/main/docs/_static/warframe_logo.jpg" alt="warframe logo" height="60"/></a></p>\n<h1 align="center">warframe-metrics</h1>\n<p align="center">Analysis tool for warframe market.</p>\n<p align="center">\n    <a href="https://pypi.org/project/warframe-metrics/"><img src="https://img.shields.io/pypi/v/warframe-metrics.svg"/></a>\n    <a href="https://warframe-metrics.readthedocs.io/en/latest/"><img src="https://readthedocs.org/projects/warframe-metrics/badge/?version=latest"/></a>\n\n</p>\n<p align="center">\n<a href="https://codecov.io/gh/rajivsarvepalli/warframe-metrics"><img src="https://codecov.io/gh/rajivsarvepalli/warframe-metrics/branch/main/graph/badge.svg?token=32T6Ok0H3X"/></a>\n<a href="https://github.com/rajivsarvepalli/warframe-metrics/actions?workflow=Tests"><img src="https://github.com/rajivsarvepalli/warframe-metrics/workflows/Tests/badge.svg"/></a>\n<a href="https://pypi.org/project/warframe-metrics/"><img src="https://img.shields.io/pypi/pyversions/warframe-metrics.svg"/></a>\n</p>\n<br/><br/>\n\n## 📈 Warframe Metrics\n\nWarframe market is an excellent tool for all of us traders. However, what about the metrics that all traders require to make intillegent desicions. This library looks\nto extend the possible analysis based on the data provided openly by warframe market.\n\n- Free software: MIT license\n\n## 📚 Documentation\n\nDocumentation is currently a work in progress.\n\n## 📦 Installing\n\nYou can install `warframe-metrics` using pip::\n\n    $ pip install warframe-metrics\n\n## 📤 Credit\n\nAll credit goes to https://warframe.market/ and their creators for enabling this project and the data used within it.\n\n## ⚙ Using\n\nComing soon...\n\n# 👷 Contributing\n\nContributions are welcome. To learn more, see the [Contributor Guide][].\n\n# 📕 License\n\nDistributed under the terms of the [MIT][] license, _warframe-metrics_ is\nfree and open source software.\n\n# 💥 Issues\n\nIf you encounter any issues or problems, please [file an issue][] along\nwith a detailed description.\n\n[contributor guide]: https://warframe-metrics.readthedocs.io/en/latest/contributor_guide/\n[mit]: http://opensource.org/licenses/MIT\n[file an issue]: https://github.com/rajivsarvepalli/warframe-metrics/issues\n',
    'author': 'Rajiv Sarvepalli',
    'author_email': 'rajiv@sarvepalli.net',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rajivsarvepalli/warframe-metrics',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)

# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['stock_trader']

package_data = \
{'': ['*']}

install_requires = \
['typer>=0.3.2,<0.4.0']

extras_require = \
{'all': ['colorama>=0.4.4,<0.5.0', 'shellingham>=1.4.0,<2.0.0'],
 'colorama': ['colorama>=0.4.4,<0.5.0'],
 'shellingham': ['shellingham>=1.4.0,<2.0.0']}

entry_points = \
{'console_scripts': ['stock_trader = stock_trader.__main__:main']}

setup_kwargs = {
    'name': 'stock-trader',
    'version': '0.0.4',
    'description': 'Stock Trader',
    'long_description': "Stock Trader\n============\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black| |Issues|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/stock_trader.svg\n   :target: https://pypi.org/project/stock_trader/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/stock_trader\n   :target: https://pypi.org/project/stock_trader\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/stock-trader\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/stock_trader/latest.svg?label=Read%20the%20Docs\n   :target: https://stock_trader.readthedocs.io/\n   :alt: Read the documentation at https://stock_trader.readthedocs.io/\n.. |Tests| image:: https://github.com/ciresnave/stock_trader/workflows/Tests/badge.svg\n   :target: https://github.com/ciresnave/stock_trader/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/ciresnave/stock_trader/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/ciresnave/stock_trader\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n.. |Issues| image:: https://img.shields.io/github/issues/CireSnave/stock_trader?style=plastic\n   :target: https://github.com/ciresnave/stock_trader/issues\n   :alt: GitHub issues\n\nOverview\n--------\n\nStock Trader retrieves historical stock data for one or more stocks, runs one or more trading\nalgorithms against the historical data optimizing algorithm settings on each pass, and picks\nthe most profitable way to trade each stock.  It then accepts a stream of current information\nabout each of the stocks watching for a buy-in point that has a high probability of profit.  \nIt then either alerts the user to buy or, alternatively, can directly send a buy order to a\nbroker's API.  It then continues to monitor the stream of current information about each of\nthe stocks watching for either a drop in the probability of continued profit of the current\nposition or for another stock's probability of profit to go higher than that of the current\nposition.  It will then either alert the user to sell the current position or, alternatively,\ncan directly send a sell order to a broker's API.\n\n\nFeatures\n--------\n\nUntil version 1.0, this should be considered a work in progress.  Not all features exist yet.\n\nPlanned features before version 1.0 are:\n\n- Generic Interface for Historical Stock Data Retrieval with several back ends\n  - TD Ameritrade (via tda-api_)\n  - More back ends will be added as time permits\n- Backtesting Interface\n  - Pluggable profit probability functions\n- Generic Broker Interface for placing orders with several back ends\n  - TD Ameritrade (via tda-api_)\n  - More back ends will be added as time permits\n\n\nDependencies\n------------\n\nPython ^3.6.1\nTyper ^0.3.2\n\nColorama ^0.4.4 (optional extra - colorizes command line interface)\nShellingham ^1.4.0 (optional extra - detects shell to make adding shell completion easier)\n\n\nInstallation\n------------\n\nYou can install *Stock Trader* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install stock_trader\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*Stock Trader* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project's skeleton was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template using `Cookiecutter`_.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/ciresnave/stock_trader/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Command-line Reference: https://stock_trader.readthedocs.io/en/latest/usage.html\n.. _yfinance: https://aroussi.com/post/python-yahoo-finance\n.. _tda-api: https://tda-api.readthedocs.io/en/latest/\n",
    'author': 'Eric Evans',
    'author_email': 'ciresnave@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ciresnave/stock_trader',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

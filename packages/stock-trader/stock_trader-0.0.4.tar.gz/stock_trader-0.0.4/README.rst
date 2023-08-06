Stock Trader
============

|PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black| |Issues|

.. |PyPI| image:: https://img.shields.io/pypi/v/stock_trader.svg
   :target: https://pypi.org/project/stock_trader/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/stock_trader
   :target: https://pypi.org/project/stock_trader
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/stock-trader
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/stock_trader/latest.svg?label=Read%20the%20Docs
   :target: https://stock_trader.readthedocs.io/
   :alt: Read the documentation at https://stock_trader.readthedocs.io/
.. |Tests| image:: https://github.com/ciresnave/stock_trader/workflows/Tests/badge.svg
   :target: https://github.com/ciresnave/stock_trader/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/ciresnave/stock_trader/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/ciresnave/stock_trader
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black
.. |Issues| image:: https://img.shields.io/github/issues/CireSnave/stock_trader?style=plastic
   :target: https://github.com/ciresnave/stock_trader/issues
   :alt: GitHub issues

Overview
--------

Stock Trader retrieves historical stock data for one or more stocks, runs one or more trading
algorithms against the historical data optimizing algorithm settings on each pass, and picks
the most profitable way to trade each stock.  It then accepts a stream of current information
about each of the stocks watching for a buy-in point that has a high probability of profit.  
It then either alerts the user to buy or, alternatively, can directly send a buy order to a
broker's API.  It then continues to monitor the stream of current information about each of
the stocks watching for either a drop in the probability of continued profit of the current
position or for another stock's probability of profit to go higher than that of the current
position.  It will then either alert the user to sell the current position or, alternatively,
can directly send a sell order to a broker's API.


Features
--------

Until version 1.0, this should be considered a work in progress.  Not all features exist yet.

Planned features before version 1.0 are:

- Generic Interface for Historical Stock Data Retrieval with several back ends
  - TD Ameritrade (via tda-api_)
  - More back ends will be added as time permits
- Backtesting Interface
  - Pluggable profit probability functions
- Generic Broker Interface for placing orders with several back ends
  - TD Ameritrade (via tda-api_)
  - More back ends will be added as time permits


Dependencies
------------

Python ^3.6.1
Typer ^0.3.2

Colorama ^0.4.4 (optional extra - colorizes command line interface)
Shellingham ^1.4.0 (optional extra - detects shell to make adding shell completion easier)


Installation
------------

You can install *Stock Trader* via pip_ from PyPI_:

.. code:: console

   $ pip install stock_trader


Usage
-----

Please see the `Command-line Reference`_ for details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Stock Trader* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project's skeleton was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template using `Cookiecutter`_.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/ciresnave/stock_trader/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Command-line Reference: https://stock_trader.readthedocs.io/en/latest/usage.html
.. _yfinance: https://aroussi.com/post/python-yahoo-finance
.. _tda-api: https://tda-api.readthedocs.io/en/latest/

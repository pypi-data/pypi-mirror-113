# XigniteGH

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/xignite-python/xignitegh/release)
![PyPI](https://img.shields.io/pypi/v/xignitegh)
![GitHub last commit](https://img.shields.io/github/last-commit/xignite-python/xignitegh)
![GitHub issues](https://img.shields.io/github/issues/xignite-python/xignitegh)
![GitHub](https://img.shields.io/github/license/xignite-python/xignitegh)

*Python module to get historical stock data from the XigniteGlobalHistorical API*

XigniteGH is a wrapper to the XigniteGlobalHistorical API. This module implements a python interface to the API provided by [Xignite](https://www.xignite.com/product/historical-stock-prices#/productoverview). A token is required.

## Install
To install the package use:
```shell
pip install xignitegh
```

## Usage
```python
import pandas as pd
from xignitegh import Xignite

xgh = Xignite(_token="TOKEN", _token_userid=USERID)

quotes = xgh.get_quotes(ticker="AAPL", years=1)
if quotes["Outcome"] == "Success":
    name = quotes["Security"]["Name"]

dividends = xgh.get_dividends(ticker="AAPL", years=1)
if dividends["Outcome"] == "Success":
    df = pd.json_normalize(dividends["CashDividends"])
```

The token may also be stored in the environment variable ``XIGNITE_TOKEN``. The token userid is optional and used only with encrypted tokens.

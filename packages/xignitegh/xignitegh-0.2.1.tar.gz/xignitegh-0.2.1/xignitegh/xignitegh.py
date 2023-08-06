import os
from datetime import date, timedelta

import requests


class Xignite(object):

    _XIGNITE_API_URL = "https://globalhistorical.xignite.com/v3/"
    _XIGNITE_QUOTES_RANGE = "xGlobalHistorical.json/GetGlobalHistoricalQuotesRange"
    _XIGNITE_CASH_DIVIDEND_HISTORY = "xGlobalHistorical.json/GetCashDividendHistory"

    def __init__(self, _token=None, _token_userid=None):

        if _token is None:
            _token = os.environ.get("XIGNITE_TOKEN")
        if not _token or not isinstance(_token, str):
            raise ValueError("The Xignite token must be provided")
        self.token = _token

        if not (_token_userid is None or isinstance(_token_userid, int)):
            raise ValueError("The Xignite userid must be a number")
        self.userid = _token_userid

    def get_quotes(self, ticker: str, years: int):

        params = {
            "IdentifierType": "Symbol",
            "Identifier": ticker,
            "IdentifierAsOfDate": "",
            "AdjustmentMethod": "All",
            "StartDate": Xignite._get_date(years_ago=years),
            "EndDate": Xignite._get_date(years_ago=0),
            "_token": self.token,
        }
        if self.userid:
            params["_token_userid"] = self.userid

        url = Xignite._XIGNITE_API_URL + Xignite._XIGNITE_QUOTES_RANGE
        response = requests.get(url=url, params=params)

        return response.json()

    def get_dividends(self, ticker: str, years: int):

        params = {
            "IdentifierType": "Symbol",
            "Identifier": ticker,
            "IdentifierAsOfDate": "",
            "CorporateActionsAdjusted": "True",
            "StartDate": Xignite._get_date(years_ago=years),
            "EndDate": Xignite._get_date(years_ago=0),
            "_token": self.token,
        }
        if self.userid:
            params["_token_userid"] = self.userid

        url = Xignite._XIGNITE_API_URL + Xignite._XIGNITE_CASH_DIVIDEND_HISTORY
        response = requests.get(url=url, params=params)

        return response.json()

    def _get_date(years_ago):

        datum = date.today() - timedelta(days=years_ago * 365)
        return datum.strftime("%m/%d/%Y")

from datetime import date, timedelta
import os
import requests


class Xignite(object):

    _XIGNITE_API_URL = "https://globalhistorical.xignite.com/v3/"
    _XIGNITE_GH = "xGlobalHistorical.json/GetGlobalHistoricalQuotesRange"

    def __init__(self, _token=None, _token_userid=None):

        if _token is None:
            _token = os.environ.get("XIGNITE_TOKEN")
        if not _token or not isinstance(_token, str):
            raise ValueError("The Xignite token must be provided")
        self._token = _token

        if _token_userid is None:
            _token_userid = os.environ.get("XIGNITE_USERID")
        if not (_token_userid is None or isinstance(_token_userid, int)):
            raise ValueError("The Xignite userid must be a number")
        self._token_userid = _token_userid

    def get_quotes(self, params={}):

        if not params:
            params = {
                "IdentifierType": "Symbol",
                "Identifier": "AAPL",
                "IdentifierAsOfDate": "",
                "AdjustmentMethod": "All",
                "StartDate": Xignite._get_date(years_ago=1),
                "EndDate": Xignite._get_date(years_ago=0),
            }
        params["_token"] = self._token
        if self._token_userid:
            params["_token_userid"] = self._token_userid
        url = Xignite._XIGNITE_API_URL + Xignite._XIGNITE_GH
        response = requests.get(url=url, params=params)
        return response.json()

    def _get_date(years_ago):

        datum = date.today() - timedelta(days=years_ago * 365)
        return datum.strftime("%m/%d/%Y")

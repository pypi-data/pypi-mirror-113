"""
Copyright (c) 2021 warada0209
This software is released under the MIT License, see LICENSE.
"""

# API仕様書
# https://calil.jp/doc/api_ref.html
import requests


class Pycalil(object):

    def __init__(self, apikey):
        self.apikey = apikey

    def library(self, pref=None, city=None, systemid=None, geocode=None, format="json", callback=" ", limit=None):
        """
        指定した条件で図書館の一覧を取得する関数
        緯度経度を指定した場合は、その地点から近い図書館を順に出力します。
        
        Parameters
        ----------
        
        pref: str
            都道府県を指定します。

        city: str
            市区町村を指定します。
            このパラメータはprefとセットで利用します

        systemid: str
            図書館のシステムIDを指定します。

        geocode: str
            緯度、経度を指定します。

        format: str
            出力形式を指定します。xmlまたはjsonです。デフォルトはxml
        
        callback: str
            JSONPのcallback関数名を指定します。
            デフォルトはcallback。JSONとして応答する場合はcallbackに空白を指定してください

        limit: int
            図書館の取得件数を指定します。
        """

        # 図書館検索エンドポイント
        library_url = "https://api.calil.jp/library"

        # parameters
        payload = {
            "appkey": self.apikey,
            "pref": pref,
            "city": city,
            "systemid": systemid,
            "geocode": geocode,
            "format": format,
            "callback": callback,
            "limit": limit,
        }

        # getリクエスト送信
        r = requests.get(library_url, params=payload)
        return r.json()

    def check(self, isbn, systemid, format="json", callback="no"):
        """
        図書館に対して蔵書の有無と貸出状況を問い合わせます。

        Parameters
        ----------
        isbn : list[int]
            書籍のISBNを指定します。
            カンマ区切りで複数指定できます。

        systemid : list[str]
            システムIDを指定します。
            カンマ区切りで複数指定できます。

        format : str
            出力形式を指定します。xmlまたはjsonです。デフォルトはjson

        callback : str
            JSONPのcallback関数名を指定します。
            デフォルトはcallback。JSONとして応答する場合はcallbackにnoを指定してください。
        """

        # 蔵書検索エンドポイント
        check_url = "https://api.calil.jp/check"

        # parameters
        payload = {
            "appkey": self.apikey,
            "isbn": ",".join(map(str, isbn)),
            "systemid": ",".join(systemid),
            "format": format,
            "callback": callback,
        }
        
        r = requests.get(check_url, params=payload)
        return r.json()

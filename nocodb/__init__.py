from __future__ import annotations
import requests
from urllib.parse import urlsplit, urljoin

from nocodb.Base import Base
from nocodb.Column import Column
from nocodb.Table import Table


import logging
_logger = logging.getLogger(__name__)
_logger.addHandler(logging.NullHandler())


API_PATH_BASE = "api/v2"


class NocoDB:
    __app_info: dict

    def __init__(self,
                 url: str,
                 api_key: str,
                 ) -> None:

        self.api_key = api_key
        self.base_url = self._get_base_url(url)
        self.api_url = urljoin(self.base_url, API_PATH_BASE) + "/"

    @staticmethod
    def _get_base_url(url) -> str:
        if API_PATH_BASE in urlsplit(url).path:
            i = url.index(API_PATH_BASE)
            url = url[:i]
        return urlsplit(url).geturl() + "/"

    def get_file(self, path, encoding: str = "utf-8") -> str:
        """Get a file from the noco server

        Args:
            path (_type_): _description_
            encoding (str, optional): Encoding of the response. Defaults to "utf-8".

        Returns:
            str: _description_

        About encoding: https://requests.readthedocs.io/en/latest/user/quickstart/#response-content
        """
        headers = {"xc-token": self.api_key}
        url = urljoin(self.base_url, path)
        r = requests.get(url=url, headers=headers)
        r.encoding = encoding

        return r.text

    def call_noco(self, path: str, method: str = "GET", **kwargs) -> requests.Response:
        headers = {"xc-token": self.api_key}
        url = urljoin(self.api_url, path)

        _logger.debug(f"Calling {method} {url} {kwargs}")
        r = requests.request(method, url, headers=headers, **kwargs)

        _logger.debug(r.status_code)

        if r.status_code >= 400:
            raise Exception(f"Server response: {r.status_code} - {r.text}")

        if r.status_code != 200:
            _logger.warning(r.text)

        return r

    def get_bases(self) -> list[Base]:
        r = self.call_noco(path="meta/bases")
        return [Base(noco_db=self, **f) for f in r.json()["list"]]

    def get_base(self, base_id: str) -> Base:
        r = self.call_noco(path=f"meta/bases/{base_id}")
        return Base(noco_db=self, **r.json())

    def get_base_by_title(self, title: str) -> Base:
        try:
            return next((b for b in self.get_bases() if b.title == title))
        except StopIteration:
            raise Exception(f"Base with name {title} not found!")

    def create_base(self, title: str, **kwargs) -> Base:
        kwargs["title"] = title

        r = self.call_noco(path="meta/bases",
                           method="POST",
                           json=kwargs)
        return self.get_base(base_id=r.json()["id"])

    def get_table(self, table_id: str) -> Table:
        r = self.call_noco(path=f"meta/tables/{table_id}")
        return Table(noco_db=self, **r.json())

    def get_column(self, column_id: str) -> Column:
        r = self.call_noco(path=f"meta/columns/{column_id}")
        return Column(noco_db=self, **r.json())

    def get_app_info(self) -> dict:
        r = self.call_noco(path="meta/nocodb/info")
        self.__app_info = r.json()
        return r.json()

    def is_cloud(self) -> bool:
        if hasattr(self, "__app_info"):
            return self.__app_info["isCloud"]
        else:
            return self.get_app_info()["isCloud"]

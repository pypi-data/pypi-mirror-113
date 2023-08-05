# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from urllib3.util import Url, parse_url
from typing import Union

from f1z1_common import is_validators, Allowed

from .base import IURL

StrOrUrl = Union[str, Url]


class RemoteURL(IURL):
    transfers = Allowed({
        "ftp": "ftp",
        "http": "http",
        "https": "https",
        "ws": "ws",
        "wss": "wss"
    })

    def __init__(self, string_or_url: StrOrUrl):
        self._raw_url = self._to_parsed_url(string_or_url)

    @property
    def raw_url(self):
        return self._raw_url

    def to_string(self) -> str:
        return self._raw_url.url

    def _to_parsed_url(self, string_or_url: StrOrUrl) -> Url:
        url: Url = None
        if self._is_parsed_url(string_or_url):
            url = string_or_url
        elif self._is_string_url(string_or_url):
            url = parse_url(string_or_url)
        else:
            raise ValueError(
                f"url need string or Url, but got {type(string_or_url).__name__}"
            )
        return self._validated_url(url)

    def _is_parsed_url(self, value):
        return isinstance(value, Url)

    def _is_string_url(self, value):
        return is_validators.is_string(value)

    def _validated_url(self, url: Url):
        scheme = url.scheme
        if not self.transfers.has(scheme):
            raise ValueError(
                f"got not support transfers {scheme}"
            )
        return url

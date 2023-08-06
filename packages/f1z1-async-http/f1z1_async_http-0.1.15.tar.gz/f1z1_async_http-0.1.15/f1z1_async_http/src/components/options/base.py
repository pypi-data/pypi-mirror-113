# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Any, Dict, TypeVar

U = TypeVar("U")


class IRequestMethod(object):
    """
    request method interface
    """

    def as_method(self) -> str:
        raise NotImplementedError("")


class IRequestOptions(object):

    def add_cookies(self, key, value):
        raise NotImplementedError("")

    def add_data(self, key, value):
        raise NotImplementedError("")

    def add_headers(self, key, value):
        raise NotImplementedError("")

    def add_json(self, key, value):
        raise NotImplementedError("")

    def add_params(self, key, value):
        raise NotImplementedError("")

    def as_dict(self) -> Dict[str, Any]:
        raise NotImplementedError("")


class IRequestURL(object):
    """
    request url interface
    """

    def as_url(self) -> U:
        raise NotImplementedError("")

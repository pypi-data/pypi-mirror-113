# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.comf
from collections import defaultdict, OrderedDict
from typing import Any, Dict, Optional


class IRequestOption(object):

    def set(self, key, value) -> None:
        raise NotImplementedError("")

    def get(self, key, default=None):
        raise NotImplementedError("")

    def as_dict(self) -> Optional[Dict]:
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


class RequestOption(IRequestOption):

    def __init__(self):
        self._option = OrderedDict()

    def get(self, key, default=None):
        return self._option.get(key, default)

    def set(self, key, value) -> None:
        self[key] = value

    def as_dict(self):
        if not self._option:
            return None
        return {key: value for key, value in self._option.items()}

    def __setitem__(self, key, value):
        self._option[key] = value

    def __getitem__(self, key):
        return self._option[key]


class RequestOptions(IRequestOptions):
    __slots__ = ["_options"]

    def __init__(self):
        self._options = defaultdict(RequestOption)

    def add_cookies(self, key, value):
        self._set("cookies", key, value)

    def add_data(self, key, value):
        self._set("data", key, value)

    def add_headers(self, key, value):
        self._set("headers", key, value)

    def add_json(self, key, value):
        self._set("json", key, value)

    def add_params(self, key, value):
        self._set("params", key, value)

    def as_dict(self) -> Dict[str, Any]:
        if not self._options:
            return {}

        return {
            key: item.as_dict()
            for key, item in self._options.items()
        }

    def _set(self, option: str, key, value):
        self[option].set(key, value)

    def __getitem__(self, key) -> IRequestOption:
        return self._options[key]

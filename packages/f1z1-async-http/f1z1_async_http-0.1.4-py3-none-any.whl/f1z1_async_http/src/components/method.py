# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from typing import AnyStr, Union

from f1z1_common import Allowed, EnumUtil, StringsUtil, Encoding, is_validators

MethodTypes = Union[AnyStr, Enum]


class IRequestMethod(object):
    """
    request method interface
    """

    def as_method(self) -> str:
        raise NotImplementedError("")


class IRequestMethodLower(object):

    def to_lower(self) -> str:
        raise NotImplementedError()


class AnyStringMethodLower(IRequestMethodLower):

    def __init__(self, method: AnyStr, encoding: Encoding = Encoding.ASCII):
        self._method = method
        self._encoding = encoding

    def to_lower(self) -> str:
        return StringsUtil.anystr_to_string(self._method, self._encoding).lower()


class EnumMethodLower(IRequestMethodLower):

    def __init__(self, method: Enum):
        self._method = method

    def to_lower(self) -> str:
        return f"{EnumUtil.unenum(self._method)}".lower()


class RequestMethod(IRequestMethod):
    allowed = Allowed({
        "delete": "DELETE",
        "get": "GET",
        "post": "POST",
        "put": "PUT"
    })

    def __init__(self, method: MethodTypes):
        self._method = self._to_lower(method)
        self._default = "get"

    def as_method(self) -> str:
        method = self._method
        if not self.allowed.has(method):
            return self.allowed.get(self._default)
        return self.allowed.get(method)

    def _to_lower(self, anystr_or_enum: MethodTypes) -> str:
        if is_validators.is_any_string(anystr_or_enum):
            return AnyStringMethodLower(anystr_or_enum).to_lower()
        elif is_validators.is_enum(anystr_or_enum):
            return EnumMethodLower(anystr_or_enum).to_lower()
        else:
            raise ValueError(f"method need anystring or Enum, but got {type(anystr_or_enum).__name__}")

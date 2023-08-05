# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from typing import AnyStr, Union

from f1z1_common import Allowed, Encoding, EnumUtil, StringsUtil, is_validators

from .base import IMethod

MethodTypes = Union[AnyStr, Enum]


class Methods(Enum):
    DELETE = "DELETE"
    GET = "GET"
    POST = "POST"
    PUT = "PUT"


class Method(IMethod):
    methods = Allowed({
        "delete": "DELETE",
        "get": "GET",
        "post": "POST",
        "put": "PUT"
    })

    def __init__(self, method: MethodTypes):
        self._method = self._to_lower_method(method)
        self._default = "get"

    @property
    def method(self):
        return self._method

    def to_string(self) -> str:
        method = self.method
        if not self.methods.has(method):
            return self.methods.get(self._default)
        return self.methods.get(method)

    def _to_lower_method(self, anystr_or_enum: MethodTypes) -> str:
        method: str = ""
        if is_validators.is_any_string(anystr_or_enum):
            method = StringsUtil.anystr_to_string(anystr_or_enum, Encoding.ASCII)
        elif is_validators.is_enum(anystr_or_enum):
            method = EnumUtil.unenum(anystr_or_enum)
        else:
            raise ValueError(f"method need string, but got {type(anystr_or_enum).__name__}")
        return method.lower()

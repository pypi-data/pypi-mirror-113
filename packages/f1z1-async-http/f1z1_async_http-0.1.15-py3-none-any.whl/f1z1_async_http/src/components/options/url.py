# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr

from httpx import URL
from f1z1_common import StringsUtil

from .base import IRequestURL


class RequestURL(IRequestURL):

    def __init__(self, any_string: AnyStr):
        self._raw = self._to_string(any_string)

    def as_url(self) -> URL:
        return URL(self._raw)

    def _to_string(self, any_string: AnyStr):
        return StringsUtil.anystr_to_string(any_string)

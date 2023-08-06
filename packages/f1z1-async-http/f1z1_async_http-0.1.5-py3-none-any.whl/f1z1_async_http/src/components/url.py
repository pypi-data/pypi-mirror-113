# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr

from httpx import URL
from f1z1_common import StringsUtil


class IRequestURL(object):
    """
    request url interface
    """

    def as_url(self) -> URL:
        raise NotImplementedError("")


class RequestURL(IRequestURL):

    def __init__(self, any_string: AnyStr):
        self._raw_url = self._to_string(any_string)

    def as_url(self):
        return URL(self._raw_url)

    def _to_string(self, any_string: AnyStr) -> str:
        return StringsUtil.anystr_to_string(any_string)

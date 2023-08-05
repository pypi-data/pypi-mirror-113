# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import defaultdict
from enum import Enum

from f1z1_common import Allowed, AsyncCallbackManager

from .base import Interceptors


class InterceptorFields(Enum):
    REQUEST = "request"
    RESPONSE = "response"


class HttpInterceptors(Interceptors):
    keys = Allowed(InterceptorFields)

    def __init__(self):
        self._interceptors = defaultdict(AsyncCallbackManager)
        self._request = InterceptorFields.REQUEST
        self._response = InterceptorFields.RESPONSE

    @property
    def request(self):
        return self._get_interceptor(self._request)

    @property
    def response(self):
        return self._get_interceptor(self._response)

    def empty(self) -> bool:
        return not self._interceptors

    def _get_interceptor(self, filed: InterceptorFields):
        return self._interceptors[self.keys.get(filed)]

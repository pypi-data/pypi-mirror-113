# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import defaultdict
from typing import Callable, Iterable

AsyncFunction = Callable
IterableAsyncFunction = Iterable[AsyncFunction]


class IInterceptorManager(object):
    """
    interceptor interface
    """

    def register(self, async_func: AsyncFunction) -> int:
        raise NotImplementedError()

    def unregister(self, async_func: AsyncFunction) -> int:
        raise NotImplementedError()

    def __iter__(self) -> IterableAsyncFunction:
        raise NotImplementedError()


class IInterceptors(object):
    """
    interceptors interface
    """

    @property
    def request(self) -> IInterceptorManager:
        raise NotImplementedError()

    @property
    def response(self) -> IInterceptorManager:
        raise NotImplementedError()


class InterceptorManager(IInterceptorManager):

    def __init__(self):
        self._list = []

    @property
    def length(self):
        return len(self._list)

    def register(self, async_func) -> int:
        if not self._is_exists(async_func):
            self._list.append(async_func)

        return self.length

    def unregister(self, async_func) -> int:
        idx = self._find(async_func)
        if idx > -1:
            self._list.pop(idx)

        return self.length

    def __iter__(self):
        if self.length:
            for _, async_cb in enumerate(self._list):
                yield async_cb

    def _is_exists(self, value) -> bool:
        return value in self._list

    def _find(self, value) -> int:
        if not self._is_exists(value):
            return -1
        return -1 if not self._is_exists(value) else self._list.index(value)


class Interceptors(IInterceptors):
    __slots__ = ["_interceptors"]

    def __init__(self):
        self._interceptors = defaultdict(InterceptorManager)

    @property
    def request(self):
        return self._get("request")

    @property
    def response(self):
        return self._get("response")

    def _get(self, key: str):
        return self._interceptors[key]

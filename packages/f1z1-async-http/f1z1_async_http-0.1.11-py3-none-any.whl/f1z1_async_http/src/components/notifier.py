# @Time     : 2021/7/16
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Optional, TypeVar

from httpx import Request, Response
from f1z1_common import is_validators

from .interceptors import IInterceptorManager
from .message import IRequestMessage

M = TypeVar("M")


class IAsyncNotifier(object):
    """
    异步消息通知器
    """

    async def notify(self, message: M) -> bool:
        raise NotImplementedError("")


class Notifier(IAsyncNotifier):

    def __init__(self, interceptors: Optional[IInterceptorManager] = None):
        self._interceptors = interceptors

    async def notify(self, message: M) -> bool:
        if self._is_not_interceptors():
            return True
        for fn in self._interceptors:
            await fn(message)
        return True

    def _is_not_interceptors(self):
        return is_validators.is_none(self._interceptors)


class NotifierDecorate(IAsyncNotifier):

    def __init__(self, interceptors: Optional[IInterceptorManager] = None):
        self._notifier = Notifier(interceptors)

    async def notify(self, message: M) -> bool:
        return await self._notifier.notify(message)


class AsyncRequestNotifier(NotifierDecorate):

    def __init__(self,
                 message: IRequestMessage,
                 interceptors: Optional[IInterceptorManager] = None):
        super().__init__(interceptors)
        self._rm = message

    async def notify(self, request: Request) -> bool:
        self._rm.add(request)
        print("add", self._rm)
        return await super().notify(request)


class AsyncResponseNotifier(NotifierDecorate):

    def __init__(self,
                 message: IRequestMessage,
                 interceptors: Optional[IInterceptorManager] = None):
        super().__init__(interceptors)
        self._rm = message

    async def notify(self, response: Response) -> bool:
        result = await super().notify(response)
        # print("pop before", self._rm)
        self._rm.pop()
        return result


def notify(notifier: IAsyncNotifier):
    async def execute(value):
        return await notifier.notify(value)

    return execute

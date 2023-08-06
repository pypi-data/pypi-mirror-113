# @Time     : 2021/7/16
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from abc import ABCMeta, abstractmethod
from typing import TypeVar

from httpx import Request, Response

from .interceptors import IInterceptorManager
from .message import IRequestMessage

M = TypeVar("M")


class AbstractAsyncNotifier(metaclass=ABCMeta):
    """
    异步消息通知器
    """

    def __init__(self, interceptors: IInterceptorManager, message: IRequestMessage):
        self._interceptors = interceptors
        self._rm = message

    @abstractmethod
    async def notify(self, message: M) -> bool:
        raise NotImplementedError("")


class AsyncRequestNotifier(AbstractAsyncNotifier):

    async def notify(self, message: Request) -> bool:
        self._rm.add(message)
        for fn in self._interceptors:
            await fn(message)


class AsyncResponseNotifier(AbstractAsyncNotifier):

    async def notify(self, message: Response) -> bool:
        for fn in self._interceptors:
            await fn(message)
        self._rm.pop()


def notify(notifier: AbstractAsyncNotifier):
    async def execute(value):
        return await notifier.notify(value)

    return execute

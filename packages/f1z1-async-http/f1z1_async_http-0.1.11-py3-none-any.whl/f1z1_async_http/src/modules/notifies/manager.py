# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Callable, Dict, List

from ..event_hook import AbstractEventHooksManager, AsyncFunction
from ..message import IRequestMessage
from .base import IAsyncNotifier
from .notifier import AsyncRequestNotifier, AsyncResponseNotifier, Notifier


class IAsyncNotifierManager(object):

    @property
    def completed(self) -> bool:
        raise NotImplementedError()

    def notify(self, notifier: IAsyncNotifier) -> AsyncFunction:
        raise NotImplementedError()

    def as_dict(self) -> Dict[str, List[Callable]]:
        raise NotImplementedError()


class AsyncNotifierManager(IAsyncNotifierManager):
    """
    通知管理器
    """

    def __init__(self, event_manager: AbstractEventHooksManager, message: IRequestMessage):
        self._em = event_manager
        self._rmq = message

    @property
    def completed(self) -> bool:
        return self._rmq.empty()

    @property
    def request(self):
        return self._em.get("request")

    @property
    def response(self):
        return self._em.get("response")

    def notify(self, notifier: IAsyncNotifier):
        async def execute(value):
            return await notifier.notify(value)

        return execute

    def as_dict(self):
        return self._as_event_hooks(self._rmq)

    def _as_event_hooks(self, message: IRequestMessage):
        notify = self.notify
        return {
            "request": [
                notify(AsyncRequestNotifier(
                    Notifier(self.request), message
                ))
            ],

            "response": [
                notify(AsyncResponseNotifier(
                    Notifier(self.response), message
                ))
            ]
        }

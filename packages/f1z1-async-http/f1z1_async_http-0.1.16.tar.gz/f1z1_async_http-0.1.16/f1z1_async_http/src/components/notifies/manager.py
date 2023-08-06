# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
try:
    import simplejson as json
except ImportError:
    import json
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

    def request(self, message: IRequestMessage):
        hooks = self._em.get("request")
        return [
            self.notify(
                AsyncRequestNotifier(Notifier(hooks), message)
            )
        ]

    def response(self, message: IRequestMessage):
        hooks = self._em.get("response")
        return [
            self.notify(
                AsyncResponseNotifier(Notifier(hooks), message)
            )
        ]

    def notify(self, notifier: IAsyncNotifier):
        async def execute(value):
            return await notifier.notify(value)

        return execute

    def as_dict(self):
        rmq = self._rmq
        return {
            "request": self.request(rmq),
            "response": self.response(rmq)
        }


    def __str__(self):
        return json.dumps(
            self.as_dict(),
            indent=2
        )
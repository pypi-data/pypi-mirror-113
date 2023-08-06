# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ..event_hook import AbstractEventHooksManager, FunctionHooksManager
from ..message import RequestMessageQueue
from .manager import IAsyncNotifierManager, AsyncNotifierManager


class INotifierManagerFactory(object):

    @classmethod
    def create(cls, event_manager: AbstractEventHooksManager = None) -> IAsyncNotifierManager:
        raise NotImplementedError("")


class NotifierManagerFactory(INotifierManagerFactory):

    @classmethod
    def create(cls, event_manager: AbstractEventHooksManager = None):
        rmq = RequestMessageQueue(2 ** 31)
        if not cls._is_manager(event_manager):
            return AsyncNotifierManager(
                FunctionHooksManager(), rmq
            )
        return AsyncNotifierManager(event_manager, rmq)

    @classmethod
    def _is_manager(cls, value):
        return isinstance(value, AbstractEventHooksManager)

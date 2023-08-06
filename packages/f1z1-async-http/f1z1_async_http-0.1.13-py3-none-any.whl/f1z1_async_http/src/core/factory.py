# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from ..components.conf import IConfig
from ..components.event_hook import AbstractEventHooksManager
from .client import IAsyncHttpClient, AsyncHttpClient
from .manager import AsyncHttpClientManager


class IAsyncHttpClientFactory(object):

    def create(self, *args, **kwargs) -> IAsyncHttpClient:
        raise NotImplementedError()


class AsyncHttpClientFactory(IAsyncHttpClientFactory):
    manager = AsyncHttpClientManager()

    def __init__(self,
                 node: str,
                 config: IConfig = None,
                 event_manager: AbstractEventHooksManager = None):
        self._node = node
        self._config = config
        self._event_manager = event_manager

    def create(self) -> IAsyncHttpClient:
        instance = AsyncHttpClientFactory.manager.get(self._node)
        if not instance:
            instance = AsyncHttpClient(self._config, self._event_manager)
            AsyncHttpClientFactory.manager.set(self._node, instance)
        return instance

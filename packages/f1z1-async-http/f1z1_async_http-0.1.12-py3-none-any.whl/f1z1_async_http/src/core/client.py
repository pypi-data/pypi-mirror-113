# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr, Optional

from httpx import Response

from ..components.conf import IConfig, Config
from ..components.event_hook import AbstractEventHooksManager
from ..components.notifies import IAsyncNotifierManager, NotifierManagerFactory
from ..components.options import IRequestOptions, MethodTypes
from .adapter import Adapters
from .aclient import AsyncClientBuilder
from .switch import AsyncSwitch


class IAsyncHttpClient(object):

    async def request(self,
                      method: MethodTypes,
                      url: AnyStr,
                      options: Optional[IRequestOptions]) -> Response:
        raise NotImplementedError("")

    async def __aenter__(self) -> ["IAsyncHttpClient"]:
        raise NotImplementedError("")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError("")


class AsyncHttpClient(IAsyncHttpClient):

    def __init__(self,
                 config: IConfig = None,
                 event_manager: AbstractEventHooksManager = None):
        self._config = config if config else Config()
        self._notifier = NotifierManagerFactory.create(event_manager)
        self._client = self._init_httpx(
            self._config,
            self._notifier
        )
        self._switch = AsyncSwitch(self._client, self._notifier)

    @property
    def client(self):
        return self._client

    def _convert(self, method: MethodTypes,
                 url: AnyStr,
                 options: Optional[IRequestOptions]):
        return Adapters(method, url, options).convert()

    async def request(self,
                      method: str,
                      url: AnyStr,
                      options: Optional[IRequestOptions]) -> Response:
        method, url, kwargs = self._convert(method, url, options)
        return await self._send(method, url, **kwargs)

    async def _send(self, method, url, **kwargs):
        return await self.client.request(method, url, **kwargs)

    async def __aenter__(self):
        await self._switch.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._switch.close()

    def _init_httpx(self,
                    config: IConfig,
                    notifier_manager: IAsyncNotifierManager):
        builder = AsyncClientBuilder()
        builder \
            .set_base_url(config.base_url) \
            .set_max_connection(config.max_connection) \
            .set_max_keepalive(config.max_keepalive) \
            .set_timeout(config.timeout) \
            .set_event_hooks(notifier_manager.as_dict())

        return builder.build()

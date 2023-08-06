# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr, Optional

from httpx import AsyncClient, Limits, Response, Timeout, URL

from ..components.conf import DEFAULT_MAX_CONNECTION, DEFAULT_MAX_KEEPALIVE, DEFAULT_TIMEOUT
from ..components.interceptors import IInterceptors, Interceptors
from ..components.method import MethodTypes
from ..components.notifier import AsyncRequestNotifier, AsyncResponseNotifier, notify
from ..components.options import IRequestOptions
from ..components.message import IRequestMessage, RequestMessageQueue
from ..modules.conf import IConfig, Config
from ..modules.event_hook import AbstractEventHooksManager
from ..modules.notifies import IAsyncNotifierManager, NotifierManagerFactory
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
                 base_url: str = "",
                 timeout: int = DEFAULT_TIMEOUT,
                 max_connection: int = DEFAULT_MAX_CONNECTION,
                 max_keepalive: int = DEFAULT_MAX_KEEPALIVE,
                 interceptors: IInterceptors = None):

        self._base_url = base_url
        self._max_connection = max_connection
        self._max_keepalive = max_keepalive
        self._timeout = timeout

        self._interceptors = interceptors if interceptors else Interceptors()
        self._rmq = RequestMessageQueue(2 ** 31)

        self._client = self._init_httpx(
            self._rmq,
            self._interceptors
        )

    @property
    def client(self):
        return self._client

    async def request(self,
                      method: MethodTypes,
                      url: AnyStr,
                      options: Optional[IRequestOptions]) -> Response:
        method, url, kwargs = self._convert(method, url, options)
        return await self._send(method, url, **kwargs)

    async def open(self):
        """
        open connection
        :return:
        """
        if self._is_closed():
            await self._client.__aenter__()

    async def close(self):
        """
        close connection
        :return:
        """
        if all([self._is_empty(), not self._is_closed()]):
            await self._client.aclose()

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _send(self, method, url, **kwargs):
        return await self.client.request(method, url, **kwargs)

    def _is_closed(self):
        return self.client.is_closed

    def _is_empty(self):
        return self._rmq.empty()

    def _convert(self, method: MethodTypes,
                 url: AnyStr,
                 options: Optional[IRequestOptions]):
        return Adapters(method, url, options).convert()

    def _init_httpx(self, message: IRequestMessage, interceptors: IInterceptors):
        return AsyncClient(
            base_url=URL(self._base_url),
            event_hooks=self._create_events(message, interceptors),
            limits=Limits(
                max_connections=self._max_connection,
                max_keepalive_connections=self._max_keepalive
            ),
            timeout=Timeout(self._timeout)
        )

    def _create_events(self, message: IRequestMessage, interceptors: IInterceptors):
        return {
            "request": [
                notify(AsyncRequestNotifier(
                    message, interceptors.request
                ))
            ],

            "response": [
                notify(AsyncResponseNotifier(
                    message, interceptors.response
                ))
            ]
        }


class AsyncHttpClient2(IAsyncHttpClient):

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

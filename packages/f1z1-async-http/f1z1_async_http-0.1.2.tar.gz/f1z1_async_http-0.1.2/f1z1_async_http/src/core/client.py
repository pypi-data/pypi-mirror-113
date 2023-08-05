# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import EnumUtil

from ._types_for_py import HttpxClient, HttpxResponse, MergedHook
from .base import IAsyncHttp
from .adapters import Adapters
from .messages import IMessages
from ..components import (
    HookManager,
    Interceptors,
    InterceptorFields,
    IOptions,
    MethodTypes,
    StrOrUrl,
    TimoutTypes
)


class AsyncHttp(IAsyncHttp):

    def __init__(self, client: HttpxClient, messages: IMessages):
        self._client = client
        self._messages = messages
        self._set_defaults(self.client)

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client) -> None:
        if not self._is_client(client):
            return
        self._set_defaults(client)
        self._client = client

    @property
    def messages(self):
        return self._messages

    @property
    def glob_timeout(self):
        return self.client.timeout

    async def request(self,
                      method: MethodTypes,
                      url: StrOrUrl,
                      *,
                      options: IOptions = None) -> HttpxResponse:
        """
        send request
        :param method:
        :param url:
        :param options:
        :return:
        """
        adapter = self._to_adaptor(
            method, url,
            glob_timeout=self.glob_timeout,
            options=options
        )
        return await self._to_request(adapter)

    def set_interceptor(self, interceptors: Interceptors) -> None:
        """
        set interceptors
        :param interceptors:
        :return:
        """
        unenum = EnumUtil.unenum
        hook = self._get_hook()
        self._merge_hook(hook, unenum(InterceptorFields.REQUEST), interceptors.request)
        self._merge_hook(hook, unenum(InterceptorFields.RESPONSE), interceptors.response)
        self._set_hook(hook)

    async def open(self):
        if self.client.is_closed:
            await self.client.__aenter__()

    async def close(self):
        # print(f"messages > {self.messages}\nstatus: {self.messages.empty()}")
        if self.messages.empty():
            return await self.client.aclose()

    def _get_hook(self) -> MergedHook:
        return self.client.event_hooks

    def _merge_hook(self, event_hooks: MergedHook, key: str, manager: HookManager) -> None:
        if not manager.empty():
            event_hooks.get(key).extend(manager)

    def _set_hook(self, new_events: MergedHook):
        self.client.event_hooks = new_events

    def _set_defaults(self, client: HttpxClient):
        self._set_default_events(client, self.messages)

    def _set_default_events(self, client: HttpxClient, messages: IMessages):
        messages.on_message(client)

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self.close()

    def _to_adaptor(self,
                    method: MethodTypes,
                    url: StrOrUrl,
                    glob_timeout: TimoutTypes = 3600,
                    options: IOptions = None) -> Adapters:
        """
        convert method, url, options
        :param method:
        :param url:
        :param glob_timeout:
        :param options:
        :return:
        """
        return Adapters(method, url, glob_timeout, options)

    async def _to_request(self, adapter: Adapters):
        method, url, options = adapter.convert()
        return await self.send(method, url, **options)

    async def send(self, method: str, url, **kwargs):
        return await self.client.request(method, url, **kwargs)

    def _is_client(self, client: HttpxClient):
        return isinstance(client, HttpxClient)

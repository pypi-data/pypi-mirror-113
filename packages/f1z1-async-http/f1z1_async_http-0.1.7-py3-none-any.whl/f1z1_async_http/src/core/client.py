# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr, Optional

from httpx import AsyncClient, Response

from ..components.method import MethodTypes
from ..components.options import IRequestOptions
from ..components.message import IRequestMessage
from .adapter import Adapters


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

    def __init__(self, client: AsyncClient, rm: IRequestMessage):
        self._client = client
        self._rm = rm

    @property
    def client(self):
        return self._client

    @client.setter
    def client(self, client: AsyncClient) -> None:
        if not self._is_client(client):
            raise ValueError(
                f"client need AsyncClient, but got {type(client).__name__}"
            )
        self._client = client

    async def request(self,
                      method: MethodTypes,
                      url: AnyStr,
                      options: Optional[IRequestOptions]) -> Response:
        method, url, kwargs = self._convert(method, url, options)
        return await self._send(method, url, **kwargs)

    async def open(self):
        if self._is_closed():
            await self._client.__aenter__()

    async def close(self):
        if all([self._is_empty(), not self._is_closed()]):
            await self._client.aclose()

    async def _send(self, method, url, **kwargs):
        return await self.client.request(method, url, **kwargs)

    def _convert(self, method: MethodTypes,
                 url: AnyStr,
                 options: Optional[IRequestOptions]):
        return Adapters(method, url, options).convert()

    def _is_closed(self):
        return self.client.is_closed

    def _is_empty(self):
        return self._rm.empty()

    def _is_client(self, client):
        return isinstance(client, AsyncClient)

    async def __aenter__(self):
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

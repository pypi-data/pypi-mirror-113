# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from httpx import AsyncClient

from ..components.notifies import IAsyncNotifierManager


class IAsyncSwitch(object):

    async def open(self) -> None:
        raise NotImplementedError()

    async def close(self) -> None:
        raise NotImplementedError()


class AsyncSwitch(IAsyncSwitch):

    def __init__(self,
                 client: AsyncClient,
                 nm: IAsyncNotifierManager):
        self._client = client
        self._notifier = nm

    async def open(self):
        if self.closed():
            await self._client.__aenter__()

    async def close(self):
        if all([self.completed(), not self.closed()]):
            # print("client, close")
            await self._client.aclose()

    def closed(self):
        return self._client.is_closed

    def completed(self):
        return self._notifier.completed

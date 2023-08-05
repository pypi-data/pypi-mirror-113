# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import deque

from ._types_for_py import HttpxClient, HttpxRequest, HttpxResponse


class IMessages(object):
    """
    messages interface
    """

    def empty(self) -> bool:
        raise NotImplementedError("NotImplemented .empty() -> bool")

    def on_message(self, client: HttpxClient, **kwargs):
        raise NotImplementedError("NotImplemented .on_message(client) -> bool")

    async def on_request(self, request: HttpxRequest, **kwargs):
        raise NotImplementedError("NotImplemented .on_request(request)")

    async def on_response(self, response: HttpxResponse, **kwargs):
        raise NotImplementedError("NotImplemented .on_response(response)")


class Messages(IMessages):
    """
    messages
    """

    def __init__(self, max_len: int = None):
        self._messages = deque(maxlen=max_len)

    def empty(self):
        return not self._messages

    def on_message(self, client: HttpxClient, **kwargs) -> None:
        hooks = client.event_hooks
        hooks.get("request").append(self.on_request)
        hooks.get("response").append(self.on_response)
        client.event_hooks = hooks

    async def on_request(self, request: HttpxRequest, **kwargs) -> None:
        self._messages.append(request)
        print("request", self._messages)

    async def on_response(self, response: HttpxResponse, **kwargs) -> None:
        if not self.empty():
            self._messages.popleft()
            print("response", self._messages)

    def __str__(self):
        return str(self._messages)

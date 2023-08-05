# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from pathlib import Path
from typing import Callable, Union

from f1z1_common import PathUtil, is_validators

from .core import HttpxResponse
from .core.client import AsyncHttp
from .core.manager import AsyncHttpManager
from .components import HttpInterceptors, Method, Options, RemoteURL, StrOrUrl, TimoutTypes


class IAsyncHttpBuilder(object):

    @property
    def node(self) -> str:
        raise NotImplementedError("NotImplemented .node -> str")

    @property
    def setting(self) -> Union[Path, None]:
        raise NotImplementedError("NotImplemented .setting -> Path")

    def add_cookies(self, key: str, value: str) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_cookies(key, value) -> IAsyncHttpBuilder")

    def add_headers(self, key: str, value: str) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_headers(key, value) -> IAsyncHttpBuilder")

    def add_data(self, key: str, value) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_data(key, value) -> IAsyncHttpBuilder")

    def add_json(self, key: str, value) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_json(key, value) -> IAsyncHttpBuilder")

    def add_params(self, key: str, value) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_params(key, value) -> IAsyncHttpBuilder")

    def add_request_interceptor(self, function: Callable) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_request_interceptor(function) -> IAsyncHttpBuilder")

    def add_response_interceptor(self, function: Callable) -> ["IAsyncHttpBuilder"]:
        raise NotImplementedError("NotImplemented .add_response_interceptor(function) -> IAsyncHttpBuilder")

    async def request(self, *args, **kwargs) -> HttpxResponse:
        raise NotImplementedError("NotImplemented .request() -> HttpxResponse")


class AsyncHttpBuilder(IAsyncHttpBuilder):

    def __init__(self, method: Union[str, Enum], url: StrOrUrl, timeout: TimoutTypes = None):
        self._method = Method(method)
        self._url = RemoteURL(url)
        self._options = Options(timeout)
        self._interceptors = HttpInterceptors()

        self._node: str = "default"
        self._setting: Path = None

    @property
    def node(self):
        return self._node

    @node.setter
    def node(self, new_node: str) -> None:
        if not is_validators.is_string(new_node):
            raise ValueError(
                f"update node, node need string, but got {type(new_node).__name__}"
            )
        self._node = new_node.lower()

    @property
    def method(self):
        return self._method

    @property
    def url(self):
        return self._url

    @property
    def options(self):
        return self._options

    @property
    def interceptors(self):
        return self._interceptors

    @property
    def setting(self):
        return self._setting

    @setting.setter
    def setting(self, new_path: Union[str, Path]) -> None:
        new_setting = PathUtil.to_path(new_path)
        if not new_setting.exists():
            raise ValueError(
                f"set new setting, but not found from {new_setting}"
            )
        self._setting = new_setting

    def add_cookies(self, key, value):
        cookies = self._options.cookies
        cookies.add(key, value)
        return self

    def add_data(self, key, value):
        data = self._options.data
        data.add(key, value)
        return self

    def add_headers(self, key, value):
        headers = self._options.headers
        headers.add(key, value)
        return self

    def add_json(self, key, value):
        json = self._options.json
        json.add(key, value)
        return self

    def add_params(self, key, value):
        params = self._options.params
        params.add(key, value)
        return self

    def add_request_interceptor(self, function: Callable):
        request = self._interceptors.request
        return request.add(function)

    def add_response_interceptor(self, function: Callable):
        response = self._interceptors.response
        return response.add(function)

    async def request(self) -> HttpxResponse:
        options = self.options
        if not options.empty():
            return await self._use_options(options)
        return await self._not_use_options()

    async def _not_use_options(self):
        return await self._send_use(
            self.node,
            self.method.to_string(),
            self.url.to_string()
        )

    async def _use_options(self, options: Options):
        return await self._send_use(
            self.node,
            self.method.to_string(),
            self.url.to_string(),
            options=options
        )

    async def _send_use(self,
                        node: str,
                        method: str,
                        url: str,
                        *,
                        options: Options = None):
        # get http
        http_node = self._get_http_from_manager(node)
        # set interceptors
        self._set_interceptors(http_node)
        # send request
        async with http_node as http:
            return await http.request(method, url, options=options)

    def _set_interceptors(self, http: AsyncHttp) -> None:
        interceptors = self.interceptors
        if not interceptors.empty():
            http.set_interceptor(interceptors)

    def _get_http_from_manager(self, node: str) -> AsyncHttp:
        manager = AsyncHttpManager(self.setting)
        if self._current_is_default(node):
            return manager.default
        return manager.get_instance(node)

    def _current_is_default(self, node: str):
        return node == "default"

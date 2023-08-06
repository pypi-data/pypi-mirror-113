# @Time     : 2021/7/17
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr

from httpx import Response
from f1z1_common import check_async_function

from ..components.conf import IConfig, ConfigManager
from ..components.interceptors import Interceptors, AsyncFunction
from ..components.method import MethodTypes
from ..components.options import RequestOptions
from .factory import AsyncHttpClientFactory
from .manager import AsyncHttpClientManager


class IAsyncRequestBuilder(object):

    def add_cookies(self, key, value) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def add_data(self, key, value) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def add_headers(self, key, value) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def add_json(self, key, value) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def add_params(self, key, value) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def set_config(self, node: str, config: IConfig) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def set_request_interceptor(self, async_function: AsyncFunction) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def set_response_interceptor(self, async_function: AsyncFunction) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    async def build(self) -> Response:
        raise NotImplementedError()


class AsyncRequestBuilder(IAsyncRequestBuilder):

    def __init__(self, method: MethodTypes, url: AnyStr):
        self._method = method
        self._url = url

        self._interceptors = Interceptors()
        self._options = RequestOptions()

        self._configs = ConfigManager()
        self._config_node = "default"

    def add_cookies(self, key, value):
        self._options.add_cookies(key, value)
        return self

    def add_data(self, key, value):
        self._options.add_data(key, value)
        return self

    def add_headers(self, key, value):
        self._options.add_headers(key, value)
        return self

    def add_json(self, key, value):
        self._options.add_json(key, value)
        return self

    def add_params(self, key, value):
        self._options.add_params(key, value)
        return self

    def set_config(self, node: str, config: IConfig):
        if not self._is_config(config):
            raise ValueError(f"config need IConfig, but got {type(config).__name__}")
        self._config_node = node
        self._configs.set(node, config)
        return self

    def set_request_interceptor(self, async_function: AsyncFunction):
        self._check_async_function(async_function)
        self._interceptors.request.register(async_function)
        return self

    def set_response_interceptor(self, async_function: AsyncFunction):
        self._check_async_function(async_function)
        self._interceptors.response.register(async_function)
        return self

    async def build(self) -> Response:
        http = self._get_instance()
        print("http id", id(http))
        async with http:
            return await http.request(self._method, self._url, self._options)

    def _get_instance(self):
        node = self._config_node
        manager = AsyncHttpClientManager()
        instance = manager.get(node)
        if not instance:
            instance = self._create_instance(node)
            manager.set(node, instance)
        return instance

    def _create_instance(self, node: str):
        config = self._configs.get(node)
        factory = AsyncHttpClientFactory(self._interceptors, config)
        return factory.create()

    def _is_config(self, value):
        return isinstance(value, IConfig)

    def _check_async_function(self, value):
        return check_async_function(value)

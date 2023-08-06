# @Time     : 2021/7/17
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr

from httpx import Response

from ..components.conf import IConfig, ConfigManager
from ..components.event_hook import AbstractEventHooksManager, FunctionHooksManager, HookOrAsyncFunc
from ..components.options import MethodTypes, RequestOptions
from .factory import AsyncHttpClientFactory


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

    def add_event_hook(self, key: str, hook_or_afunc: HookOrAsyncFunc) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def set_config(self, node: str, config: IConfig) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    def set_event_manager(self, event_manager: AbstractEventHooksManager) -> ["IAsyncRequestBuilder"]:
        raise NotImplementedError("")

    async def build(self) -> Response:
        raise NotImplementedError()


class AsyncRequestBuilder(IAsyncRequestBuilder):

    def __init__(self, method: MethodTypes, url: AnyStr):
        self._method = method
        self._url = url
        self._options = RequestOptions()

        self._configs = ConfigManager()
        self._config_node = "default"
        self._event_manager = FunctionHooksManager()

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

    def add_event_hook(self, key: str, hook_or_afunc: HookOrAsyncFunc):
        self._event_manager.set(key, hook_or_afunc)
        return self

    def set_config(self, node: str, config: IConfig):
        self._check_config(config)
        self._config_node = node
        self._configs.set(node, config)
        return self

    def set_event_manager(self, event_manager: AbstractEventHooksManager):
        self._check_event_manager(event_manager)
        self._event_manager = event_manager
        return self

    async def build(self) -> Response:
        http = self._get_instance()
        # print("http id", id(http))
        async with http:
            return await http.request(self._method, self._url, self._options)

    def _get_instance(self):
        node = self._config_node
        config = self._configs.get(node)
        factory = AsyncHttpClientFactory(node, config, self._event_manager)
        return factory.create()

    def _check_config(self, value):
        if not isinstance(value, IConfig):
            raise ValueError(f"config need IConfig, but got {type(value).__name__}")

    def _check_event_manager(self, value):
        if not isinstance(value, AbstractEventHooksManager):
            raise ValueError(f"interceptors need AbstractEventHooksManager, but got {type(value).__name__}")

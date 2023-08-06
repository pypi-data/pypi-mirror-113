# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from httpx import AsyncClient, URL, Timeout, Limits
from f1z1_common import ReaderFactory, PathTypes, Encoding

from ..components.conf import IConfig, DefaultConfig, ConfigReader, ConfigGenerator
from ..components.interceptors import IInterceptors
from ..components.message import IRequestMessage, RequestMessageQueue
from ..components.notifier import AsyncRequestNotifier, AsyncResponseNotifier, notify
from .client import IAsyncHttpClient, AsyncHttpClient


class IConfigFactory(object):

    @classmethod
    def create(cls, file: PathTypes, node: str) -> IConfig:
        raise NotImplementedError()


class ConfigFactory(IConfigFactory):

    @classmethod
    def create(cls, file: PathTypes, node: str) -> IConfig:
        reader = ReaderFactory.create(file, encoding=Encoding.UTF_8)
        config_reader = ConfigReader(reader, node)
        generator = ConfigGenerator(config_reader)
        return generator.generate()


class IAsyncHttpClientFactory(object):

    def create(self) -> IAsyncHttpClient:
        raise NotImplementedError()


class AsyncHttpClientFactory(IAsyncHttpClientFactory):

    def __init__(self, interceptors: IInterceptors, config: IConfig = None):
        self._interceptors = interceptors
        self._config = DefaultConfig() if not config else config

    def create(self) -> IAsyncHttpClient:
        rmq = RequestMessageQueue()
        client = self._create_async_client_from(rmq)
        return AsyncHttpClient(client, rmq)

    def _create_async_client_from(self, message: IRequestMessage):
        config = self._config
        return AsyncClient(
            base_url=self._create_base_url(config),
            limits=self._create_limits(config),
            timeout=self._create_timeout(config),
            event_hooks=self._events_hooks(message)
        )

    def _create_base_url(self, config: IConfig):
        return URL(config.base_url)

    def _events_hooks(self, message: IRequestMessage):
        interceptors = self._interceptors
        return {
            "request": [
                notify(AsyncRequestNotifier(
                    interceptors.request, message
                ))
            ],

            "response": [
                notify(AsyncResponseNotifier(
                    interceptors.response, message
                ))
            ]
        }

    def _create_limits(self, config: IConfig):
        return Limits(
            max_connections=config.max_connection,
            max_keepalive_connections=config.max_keepalive
        )

    def _create_timeout(self, config: IConfig):
        return Timeout(config.timeout)

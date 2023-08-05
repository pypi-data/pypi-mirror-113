# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from httpx import AsyncClient, URL, Timeout, Limits

from .base import IAsyncHttpFactory
from .client import AsyncHttp
from .messages import Messages
from ..conf import IConfig


class AsyncHttpFactory(IAsyncHttpFactory):

    @classmethod
    def create(cls, config: IConfig, **kwargs):
        client = cls.create_async_client_from(config)
        messages = Messages()
        return AsyncHttp(client, messages)

    @classmethod
    def create_async_client_from(cls, config: IConfig):
        return AsyncClient(
            base_url=cls._create_base_url(config),
            limits=cls._create_limits(config),
            timeout=cls._create_timeout(config)
        )

    @classmethod
    def _create_base_url(cls, config: IConfig):
        return URL(config.base_url)

    @classmethod
    def _create_timeout(cls, config: IConfig):
        return Timeout(config.timeout)

    @classmethod
    def _create_limits(cls, config: IConfig):
        return Limits(
            max_connections=config.max_connection,
            max_keepalive_connections=config.max_keepalive
        )

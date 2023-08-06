# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import ReaderFactory, PathTypes, Encoding

from ..components.interceptors import IInterceptors
from .conf import IConfig, Config, ConfigReader, ConfigGenerator
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

    @classmethod
    def create(cls, *args, **kwargs) -> IAsyncHttpClient:
        raise NotImplementedError()


class AsyncHttpClientFactory(IAsyncHttpClientFactory):

    @classmethod
    def create(cls, config: IConfig = None, interceptors: IInterceptors = None) -> IAsyncHttpClient:
        config = Config() if not config else config
        return AsyncHttpClient(
            base_url=config.base_url,
            max_connection=config.max_connection,
            max_keepalive=config.max_keepalive,
            timeout=config.timeout,
            interceptors=interceptors
        )

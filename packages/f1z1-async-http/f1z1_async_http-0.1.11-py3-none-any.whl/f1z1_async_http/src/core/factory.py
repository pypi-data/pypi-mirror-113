# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
# from ..components.conf import IConfig, Config
# from ..components.interceptors import IInterceptors
from ..modules.conf import IConfig
from ..modules.event_hook import AbstractEventHooksManager
# from .client import IAsyncHttpClient, AsyncHttpClient, AsyncHttpClient2
from .client import IAsyncHttpClient, AsyncHttpClient2

class IAsyncHttpClientFactory(object):

    @classmethod
    def create(cls, *args, **kwargs) -> IAsyncHttpClient:
        raise NotImplementedError()


# class AsyncHttpClientFactory(IAsyncHttpClientFactory):
#
#     @classmethod
#     def create(cls, config: IConfig = None, interceptors: IInterceptors = None) -> IAsyncHttpClient:
#         config = Config() if not config else config
#         return AsyncHttpClient(
#             base_url=config.base_url,
#             max_connection=config.max_connection,
#             max_keepalive=config.max_keepalive,
#             timeout=config.timeout,
#             interceptors=interceptors
#         )


class AsyncHttpClient2Factory(IAsyncHttpClientFactory):

    @classmethod
    def create(cls,
               config: IConfig = None,
               event_manager: AbstractEventHooksManager = None) -> IAsyncHttpClient:
        return AsyncHttpClient2(config, event_manager)

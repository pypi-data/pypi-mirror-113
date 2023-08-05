# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Optional, TypeVar

from ._types_for_py import HttpxResponse
from ..components import Interceptors, IOptions, MethodTypes

T = TypeVar("T")


class IAdapters(object):
    """
    converter interface
    """

    def convert(self, *args, **kwargs) -> T:
        raise NotImplementedError("NotImplemented .convert() -> T")


class IAsyncHttp(object):
    """
    async http client interface
    """

    async def request(self,
                      method: MethodTypes,
                      url: str, *,
                      options: Optional[IOptions] = None) -> HttpxResponse:
        """
        send request to server
        :param method: string or bytes
        :param url: str
        :param options: Optional[IOptional] = None
        :return: HttpResponse
        """
        raise NotImplementedError("NotImplemented .request")

    def set_interceptor(self, interceptors: Interceptors) -> None:
        """
        set interceptors to request
        :param interceptors: Interceptors
        :return: None
        """
        raise NotImplementedError("NotImplemented .set_interceptor(interceptors) -> None")


class IAsyncHttpFactory(object):

    @classmethod
    def create(cls, *args, **kwargs) -> IAsyncHttp:
        raise NotImplementedError("NotImplemented .create(config) -> IAsyncHttp")


class IAsyncHttpManager(object):

    def get_instance(self, name, **kwargs) -> IAsyncHttp:
        raise NotImplementedError("NotImplemented .get_instance(name: str) -> IAsyncHttp")

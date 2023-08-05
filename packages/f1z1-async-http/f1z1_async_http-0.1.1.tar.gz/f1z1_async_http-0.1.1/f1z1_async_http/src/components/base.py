# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Dict, Union

from f1z1_common import AsyncCallbackManager

TimoutTypes = Union[int, float]
HookManager = AsyncCallbackManager


class IMethod(object):
    """
    method interface
    """

    def to_string(self) -> str:
        raise NotImplementedError("NotImplemented .to_string() -> str")


class IURL(object):
    """
    url interface
    """

    def to_string(self) -> str:
        raise NotImplementedError("NotImplemented .to_string() -> str")


class Interceptors(object):
    """
    interceptors interface
    """

    @property
    def request(self) -> HookManager:
        raise NotImplementedError("NotImplemented .request -> AsyncCallbackManager")

    @property
    def response(self) -> HookManager:
        raise NotImplementedError("NotImplemented .response -> AsyncCallbackManager")

    def empty(self) -> bool:
        """
        interceptors is empty
        :return:
        """
        raise NotImplementedError("NotImplemented .empty() -> bool")


class IOption(object):
    """
    optional interface
    """

    def to_dict(self) -> Dict:
        """
        data to dict
        :return:
        """
        raise NotImplementedError("NotImplemented .to_dict() -> Dict")

    def add(self, key, value) -> None:
        """
        add option to IOptional
        :param key:
        :param value:
        :return:
        """
        raise NotImplementedError("NotImplemented .set(key, value) -> None")


class IOptions(object):
    """
    options interface
    """

    @property
    def cookies(self) -> IOption:
        """
        cookies option
        :return: IOptional or None
        """
        raise NotImplementedError("NotImplemented .cookies -> IOptional or None")

    @property
    def data(self) -> IOption:
        """
        data option
        :return: IOptional or None
        """
        raise NotImplementedError("NotImplemented .data -> IOptional or None")

    @property
    def headers(self) -> IOption:
        """
        headers option
        :return: IOptional or None
        """
        raise NotImplementedError("NotImplemented .headers -> IOptional or None")

    @property
    def json(self) -> IOption:
        """
        json option
        :return: IOptional or None
        """
        raise NotImplementedError("NotImplemented .json -> IOptional or None")

    @property
    def params(self) -> IOption:
        """
        params option
        :return: IOptional or None
        """
        raise NotImplementedError("NotImplemented .params -> IOptional or None")

    @property
    def timeout(self) -> Union[TimoutTypes, None]:
        """
        timeout option
        :return:
        """
        raise NotImplementedError("NotImplemented .timeout -> TimoutTypes")

    def empty(self) -> bool:
        """
        options is empty
        :return:
        """
        raise NotImplementedError("NotImplemented .empty() -> bool")

# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from pathlib import Path
from typing import Union


class IConfig(object):

    @property
    def base_url(self) -> str:
        """
        base url config
        :return:
        """
        raise NotImplementedError("NotImplemented .base_url -> str")

    @property
    def max_connection(self) -> int:
        """
        connect pool max connection
        :return:
        """
        raise NotImplementedError("NotImplemented .max_connection -> int")

    @property
    def max_keepalive(self) -> int:
        """
        connect pool max keepalive
        :return:
        """
        raise NotImplementedError("NotImplemented .max_keepalive -> int")

    @property
    def timeout(self) -> Union[int, float]:
        """
        timeout
        :return:
        """
        raise NotImplementedError("NotImplemented .timeout -> int or float")

    def set_node(self, node: str) -> None:
        raise NotImplementedError("NotImplemented .set_node(node) -> None")


class IConfigGenerator(object):

    @classmethod
    def generate_from_ini(cls, file: Path, **kwargs) -> IConfig:
        raise NotImplementedError("NotImplemented .generate_from_ini(filename) -> IHttpConfig")

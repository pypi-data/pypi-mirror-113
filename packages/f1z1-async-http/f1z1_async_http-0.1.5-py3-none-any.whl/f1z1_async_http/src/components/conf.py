# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from collections import defaultdict
from typing import Union

from f1z1_common import AbstractConfReader


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


class IConfReader(object):

    def read_base_url(self) -> str:
        raise NotImplementedError("")

    def read_timeout(self) -> Union[int, float]:
        raise NotImplementedError("")

    def read_max_connection(self) -> int:
        raise NotImplementedError("")

    def read_max_keepalive(self) -> int:
        raise NotImplementedError("")


class IConfigGenerator(object):

    def generate(self) -> IConfig:
        raise NotImplementedError("")


class IConfigManager(object):

    def set(self, node: str, config: IConfig):
        raise NotImplementedError("")

    def get(self, node: str) -> IConfig:
        raise NotImplementedError("")


class DefaultConfig(IConfig):

    def __init__(self,
                 base_url: str = None,
                 timeout: Union[int, float] = None,
                 max_connection: int = None,
                 max_keepalive: int = None):
        self._base_url = "" if not base_url else base_url
        self._timeout = 3600 if not timeout else timeout
        self._max_connection = 100 if not max_connection else max_connection
        self._max_keepalive = 20 if not max_keepalive else max_keepalive

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def max_connection(self) -> int:
        return abs(self._max_connection)

    @property
    def max_keepalive(self) -> int:
        return abs(self._max_keepalive)

    @property
    def timeout(self) -> Union[int, float]:
        return abs(self._timeout)


class ConfigManager(IConfigManager):
    __slots__ = [
        "_configs"
    ]

    def __init__(self):
        self._configs = defaultdict(DefaultConfig)

    def get(self, node: str) -> IConfig:
        return self[node]

    def set(self, node: str, config: IConfig):
        self[node] = config

    def __getitem__(self, item):
        return self._configs[item]

    def __setitem__(self, key, value: IConfig):
        self._configs[key] = value


class ConfigReader(IConfReader):

    def __init__(self, reader: AbstractConfReader, node: str):
        self._node = node
        self._reader = reader

    def read_base_url(self) -> str:
        return self._reader.get_string(self._node, "BASE_URL")

    def read_timeout(self) -> Union[int, float]:
        return self._reader.get_float(self._node, "TIMEOUT")

    def read_max_connection(self) -> int:
        return self._reader.get_int(self._node, "MAX_CONNECTION")

    def read_max_keepalive(self) -> int:
        return self._reader.get_int(self._node, "MAX_KEEPALIVE")


class ConfigGenerator(IConfigGenerator):

    def __init__(self, reader: IConfReader):
        self._reader = reader

    def generate(self) -> IConfig:
        config_reader = self._reader
        return DefaultConfig(
            base_url=config_reader.read_base_url(),
            timeout=config_reader.read_timeout(),
            max_connection=config_reader.read_max_connection(),
            max_keepalive=config_reader.read_max_keepalive()
        )

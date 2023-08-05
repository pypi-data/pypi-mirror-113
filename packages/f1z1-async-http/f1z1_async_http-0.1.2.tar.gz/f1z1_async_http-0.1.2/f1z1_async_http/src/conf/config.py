# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from typing import Union

from f1z1_common import Allowed, AbstractConfReader, is_validators

from .base import IConfig


class ConfigOptions(Enum):
    BASE_URL = "BASE_URL"
    MAX_CONNECTION = "MAX_CONNECTION"
    MAX_KEEPALIVE = "MAX_KEEPALIVE"
    TIMEOUT = "TIMEOUT"


class Config(IConfig):
    options = Allowed(ConfigOptions)

    def __init__(self, reader: AbstractConfReader):
        self._reader = reader
        self._node = "DEFAULT"

    def set_node(self, node: str) -> None:
        if not is_validators.is_string(node):
            raise ValueError(f"config node need string, but got {type(node).__name__}")
        self._node = node.upper()

    @property
    def base_url(self) -> str:
        return self._reader.get_string(self._node, self._get_config_option(ConfigOptions.BASE_URL))

    @property
    def max_connection(self) -> int:
        return self._reader.get_int(self._node, self._get_config_option(ConfigOptions.MAX_CONNECTION))

    @property
    def max_keepalive(self) -> int:
        return self._reader.get_int(self._node, self._get_config_option(ConfigOptions.MAX_KEEPALIVE))

    @property
    def timeout(self) -> Union[int, float]:
        return self._reader.get_float(self._node, self._get_config_option(ConfigOptions.TIMEOUT))

    def _get_config_option(self, option: ConfigOptions):
        return self.options.get(option)

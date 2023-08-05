# @Time     : 2021/6/1
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from enum import Enum
from pathlib import Path

from f1z1_common import Allowed, is_validators

from .base import IAsyncHttp, IAsyncHttpManager
from .factory import AsyncHttpFactory
from ..conf import ConfigGenerator


class Defaults(Enum):
    INSTANCE = "default"
    SETTING_FILE_NAME = "settings.ini"


class AsyncHttpManager(IAsyncHttpManager):
    __shared = {}  # shared states

    __defaults = Allowed(Defaults)  # defaults

    def __init__(self, file: Path = None):
        self.__dict__ = AsyncHttpManager.__shared
        self._settings = self.to_settings(file)
        self._default = self._create_default()

    @property
    def default(self):
        return self._default

    @property
    def settings(self):
        return self._settings

    def get_instance(self, node: str = "default", **kwargs):
        instance = self._get(node)
        if not is_validators.is_none(instance):
            return instance
        instance = self._create(node)
        self._register(node, instance)
        return instance

    def _create_default(self):
        return self._create(self._get_defaults(Defaults.INSTANCE))

    def to_settings(self, file: Path = None):
        settings: Path = None
        if is_validators.is_none(file):
            settings = self._get_default_settings()
        else:
            settings = file
        # print(f"settings file {settings}")
        return settings

    def _get(self, node: str):
        """
        get async http
        :param node:
        :return:
        """
        return getattr(self, node, None)

    def _register(self, node: str, instance: IAsyncHttp):
        """
        register async http
        :param node:
        :param instance:
        :return:
        """
        setattr(self, node, instance)

    def _create(self, node: str):
        """
        create async http
        :param node:
        :return:
        """
        # reader config
        config = ConfigGenerator.generate_from_ini(self.settings)
        # set node
        config.set_node(node)
        return AsyncHttpFactory.create(config)

    def _get_default_settings(self):
        file = self._get_defaults(Defaults.SETTING_FILE_NAME)
        return Path.cwd().joinpath(file)

    def _get_defaults(self, key: Defaults) -> str:
        return self.__defaults.get(key)

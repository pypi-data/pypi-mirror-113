# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from f1z1_common import ReaderFactory

from .base import IConfigGenerator
from .config import Config


class ConfigGenerator(IConfigGenerator):

    @classmethod
    def generate_from_ini(cls, file, **kwargs):
        """
        create config from config file
        :param file: Path
        :param kwargs:
        :return:
        """
        reader = ReaderFactory.create(file)
        return Config(reader)

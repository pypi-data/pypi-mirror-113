# @Time     : 2021/7/18
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Deque, TypeVar

from httpx import Request

T = TypeVar("T")
RMQ = Deque[Request]


class IRequestMessage(object):

    def empty(self):
        raise NotImplementedError()

    def add(self, message: T) -> None:
        """
        添加消息
        :param message:
        :return:
        """
        raise NotImplementedError()

    def pop(self) -> T:
        """
        移除消息
        :return:
        """
        raise NotImplementedError()

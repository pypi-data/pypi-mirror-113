# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr

from f1z1_common import is_validators

from ..components.method import RequestMethod, MethodTypes
from ..components.options import IRequestOptions
from ..components.url import RequestURL


class IAdapter(object):

    def convert(self):
        raise NotImplementedError()


class MethodAdapter(IAdapter):

    def __init__(self, method: MethodTypes):
        self._method = RequestMethod(method)

    def convert(self):
        return self._method.as_method()


class URLAdapter(IAdapter):

    def __init__(self, any_string: AnyStr):
        self._url = RequestURL(any_string)

    def convert(self):
        return self._url.as_url()


class OptionsAdapter(IAdapter):

    def __init__(self, options: IRequestOptions = None):
        self._options = options

    def convert(self):
        return self._as_dict()

    def _as_dict(self):
        return {} if is_validators.is_none(self._options) else self._options.as_dict()

    def _is_not_options(self, options):
        return True if is_validators.is_none(options) else options.empty()


class Adapters(IAdapter):

    def __init__(self,
                 method: MethodTypes,
                 url: AnyStr,
                 options: IRequestOptions = None):
        self._method = MethodAdapter(method)
        self._url = URLAdapter(url)
        self._options = OptionsAdapter(options)

    def convert(self):
        return self._as_method(), self._as_url(), self._as_kwargs()

    def _as_method(self):
        return self._method.convert()

    def _as_url(self):
        return self._url.convert()

    def _as_kwargs(self):
        return self._options.convert()

# @Time     : 2021/5/31
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import AnyStr, Dict, Union

from httpx import URL, Cookies, Headers, QueryParams, Timeout
from f1z1_common import is_validators

from ._types_for_py import MergedResult
from .base import IAdapters
from ..components import IMethod, IURL, IOption, IOptions, TimoutTypes

ToMethodTypes = Union[AnyStr, IMethod]
ToURLTypes = Union[AnyStr, IURL]
ToOptionTypes = Union[None, IOptions]
ToTimeTypes = Union[TimoutTypes, Timeout]


class MethodAdapter(IAdapters):

    def __init__(self, method: ToMethodTypes):
        self._method = self._to_anystr(method)

    def convert(self) -> AnyStr:
        return self._method

    def _to_anystr(self, method: ToMethodTypes) -> AnyStr:
        if self._is_method(method):
            return method.to_string()
        elif is_validators.is_any_string(method):
            return method
        else:
            raise ValueError(
                f"method need string, enum, or Method, bug got {type(method).__name__}"
            )

    def _is_method(self, method):
        return isinstance(method, IMethod)


class URLAdapter(IAdapters):

    def __init__(self, url: ToURLTypes):
        self._url = self._to_anystr(url)

    def convert(self) -> URL:
        return URL(self._url)

    def _to_anystr(self, url: ToURLTypes) -> AnyStr:
        if self._is_url(url):
            return url.to_string()
        elif is_validators.is_any_string(url):
            return url
        else:
            raise ValueError(
                f"url need a string or HttpURL, but got {type(url).__name__}"
            )

    def _is_url(self, value):
        return isinstance(value, IURL)


class OptionsAdapter(IAdapters):

    def __init__(self,
                 glob_timeout: ToTimeTypes,
                 options: IOptions = None):
        self._glob_timout = glob_timeout
        self._options = options

    def convert(self):
        return self._to_options(self._options)

    def _to_options(self, options: IOptions):
        if self._is_not_options(options):
            return {}
        return {
            "cookies": self._to_cookies(options),
            "headers": self._to_headers(options),
            "data": self._to_data(options),
            "json": self._to_json(options),
            "params": self._to_params(options),
            "timeout": self._to_timeout(options)
        }

    def _to_cookies(self, options: IOptions):
        return Cookies(self._to_dict(options.cookies))

    def _to_data(self, options: IOptions):
        return self._to_dict(options.data)

    def _to_headers(self, options: IOptions):
        return Headers(self._to_dict(options.headers))

    def _to_json(self, options: IOptions):
        return self._to_dict(options.json)

    def _to_params(self, options: IOptions):
        return QueryParams(self._to_dict(options.params))

    def _to_timeout(self, options: IOptions):
        timeout = options.timeout
        if timeout:
            self._glob_timout = timeout
        return Timeout(self._glob_timout)

    def _to_dict(self, option: IOption) -> Dict:
        return {} if not self._is_optional(option) else option.to_dict()

    def _is_optional(self, option):
        return isinstance(option, IOption)

    def _is_not_options(self, options):
        return True if is_validators.is_none(options) else options.empty()


class Adapters(IAdapters):

    def __init__(self,
                 method: ToMethodTypes,
                 url: ToURLTypes,
                 glob_timeout: ToTimeTypes,
                 options: IOptions = None):
        self._method = MethodAdapter(method)
        self._url = URLAdapter(url)
        self._options = OptionsAdapter(glob_timeout, options)

    def convert(self) -> MergedResult:
        method = self._method
        url = self._url
        options = self._options
        return method.convert(), url.convert(), options.convert()

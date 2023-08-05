# @Time     : 2021/5/30
# @Project  : f1z1-g
# @IDE      : PyCharm
# @Author   : Angel
# @Email    : 376355670@qq.com
from typing import Callable, Dict, List, Tuple
from httpx import Request, Response, URL, AsyncClient

HttpxClient = AsyncClient
HttpxRequest = Request
HttpxResponse = Response
HttpxURL = URL

MergedHook = Dict[str, List[Callable]]
MergedResult = Tuple[str, URL, Dict]

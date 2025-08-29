from collections.abc import Mapping, Sequence
import logging
from functools import cached_property

import aiohttp

from .data import crawl_for_key
from .url import compose_url


#logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


type JsonPrimitives = str | int | float | bool | None
type Json = Mapping[str, Json | JsonPrimitives] | Sequence[Json | JsonPrimitives]
type JsonObject = Mapping[str, Json | JsonPrimitives]


class UrlDependencies():
    def __init__(self):
        pass

    @cached_property
    def session(self):
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5))

    async def get(self, *args, **kwargs) -> aiohttp.ClientResponse:
        #log.info(params.url)
        async with self.session.get(*args, ssl=False, **kwargs) as response:
            return response

    async def get_dependencies(self, url='') -> Json:
        response = await self.get(url)
        breakpoint()
        return {'a': 1}

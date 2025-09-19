from collections.abc import Sequence, Iterable
import logging
from functools import cached_property, partial
from itertools import chain
from typing import Tuple
import asyncio

import aiohttp
from bs4 import BeautifulSoup
from async_lru import alru_cache
import ujson

from .data import crawl_for_str_value
from .url import relative_to_absolute_url, is_absolute_url


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


type Headers = Iterable[Tuple[str,str]]

class UrlDependencies:
    def __init__(self):
        pass

    @cached_property
    def session(self):
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5))

    async def get(self, *args, **kwargs) -> Tuple[aiohttp.ClientResponse, bytes]:
        log.info(args)
        async with self.session.get(*args, ssl=False, **kwargs) as response:
            return (response, await response.content.read())

    @alru_cache(ttl=5*60)
    async def get_dependencies_for_url(self, url, headers:Headers=()) -> Iterable[str]:
        log.info(f'GET: {url=} {headers=}')
        response, response_content = await self.get(url, headers=dict(headers))
        if "html" in response.content_type:
            html = BeautifulSoup(response_content, "html.parser")
            dependency_urls = filter(None, chain(
                (link.get('href') for link in html.find_all("link")),  # css and some js  # , rel="stylesheet"
                (img.get('src') for img in html.find_all("img")),  # img
                (script.get('src') for script in html.find_all("script")),  # js
            ))
            dependency_urls = tuple(dependency_urls)
            return frozenset(map(partial(relative_to_absolute_url, url), dependency_urls))
        if "json" in response.content_type:
            return frozenset(crawl_for_str_value(ujson.loads(response_content), is_absolute_url))
        raise Exception(f"unsupported {response.content_type=} for {url=}")

    async def get_dependencies(self, urls:Iterable[str]=(), headers:Headers=(), **kwargs) -> Sequence[str]:
        dependencies = await asyncio.gather(*(  # fetch all urls in parallel
            self.get_dependencies_for_url(url, headers=headers)
            for url in urls
        ))#, return_exceptions=True)  # TODO: prevent one exception tanking the whole request
        return tuple(frozenset(chain.from_iterable(dependencies)))

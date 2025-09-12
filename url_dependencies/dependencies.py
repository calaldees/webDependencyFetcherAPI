from collections.abc import Mapping, Sequence, Iterable, Set
import logging
from functools import cached_property, partial
from itertools import chain
from typing import Tuple

import aiohttp
from bs4 import BeautifulSoup

from .data import crawl_for_key
from .url import compose_url, relative_to_absolute_url


# logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


type JsonPrimitives = str | int | float | bool | None
type Json = Mapping[str, Json | JsonPrimitives] | Sequence[Json | JsonPrimitives]
type JsonObject = Mapping[str, Json | JsonPrimitives]


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

    async def get_dependencies_for_url(self, url) -> Iterable[str]:
        response, response_content = await self.get(url)
        if "html" in response.content_type:
            html = BeautifulSoup(response_content, "html.parser")
            dependency_urls = filter(None, chain(
                (link.get('href') for link in html.find_all("link", rel="stylesheet")),  # css
                (img.get('src') for img in html.find_all("img")),  # img
                (script.get('src') for script in html.find_all("script")),  # js
            ))
            dependency_urls = tuple(dependency_urls)
            return frozenset(map(partial(relative_to_absolute_url, url), dependency_urls))
        raise Exception(f"unsupported {response.content_type=} for {url=}")

    async def get_dependencies(self, urls=(), **kwargs) -> Mapping[str, Sequence[str]]:
        return {url: tuple(await self.get_dependencies_for_url(url)) for url in urls}

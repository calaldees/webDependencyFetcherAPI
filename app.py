#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "sanic[ext]",
#   "ujson",
#   "aiohttp",
#   "beautifulsoup4",
#   "async-lru",
# ]
# ///

from collections import ChainMap
from pathlib import Path

import sanic
from sanic.log import logger as log

from url_dependencies.dependencies import UrlDependencies
deps = UrlDependencies()

#import logging
#logging.basicConfig(level=logging.DEBUG)

app = sanic.Sanic("webDependencyFetcherAPI")
app.config.FALLBACK_ERROR_FORMAT = 'json'

app.config.README = Path("README.md").read_text()
@app.route("/")
async def root(request: sanic.Request) -> sanic.HTTPResponse:
    return sanic.response.text(app.config.README)
@app.route("/favicon.ico")
async def favicon(request: sanic.Request) -> sanic.HTTPResponse:
    return sanic.response.convenience.empty()  # suppress browser exception spam

@app.route('/dependenciesOf', methods=["GET", "POST"])
async def dependenciesOf(request: sanic.Request) -> sanic.HTTPResponse:
    ALLOWED_HEADERS = frozenset(('accept',))
    kwargs = ChainMap(
        {'headers': tuple((k,v) for k,v in request.headers.items() if k.lower() in ALLOWED_HEADERS)},
        {k:request.args.get(k) for k in request.args.keys()} or {},
        request.json if 'json' in request.content_type else {},
        request.form if 'form' in request.content_type else {},
    )
    log.info(kwargs)
    return sanic.response.json((await deps.get_dependencies(**kwargs)) or {})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, access_log=False, single_process=True, debug=True)

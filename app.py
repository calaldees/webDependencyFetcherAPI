#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "sanic[ext]",
#   "ujson",
#   "aiohttp",
#   "beautifulsoup4",
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

@app.route('/thing', methods=["GET", "POST"])
async def thing(request: sanic.Request) -> sanic.HTTPResponse:
    kwargs = ChainMap({k:request.args.get(k) for k in request.args.keys()} or {}, request.json or {})
    log.info(kwargs)
    return sanic.response.json((await deps.get_dependencies(**kwargs)) or {})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, access_log=False, single_process=True, debug=True)

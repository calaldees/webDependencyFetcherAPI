#!/usr/bin/env -S uv run --script
# /// script
# dependencies = [
#   "sanic[ext]",
#   "ujson",
#   "aiohttp",
#   "beautifulsoup4",
# ]
# ///

from pathlib import Path
import logging

import sanic
#from sanic.log import logger as log

logging.basicConfig(level=logging.DEBUG)


app = sanic.Sanic("webDependencyFetcherAPI")
app.config.FALLBACK_ERROR_FORMAT = 'json'

app.config.README = Path("README.md").read_text()
@app.route("/")
async def root(request) -> sanic.HTTPResponse:
    return sanic.response.text(app.config.README)
@app.route("/favicon.ico")
async def favicon(request) -> sanic.HTTPResponse:
    return sanic.response.convenience.empty()  # suppress browser exception spam

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, access_log=True, single_process=True)

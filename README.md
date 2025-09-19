webDependencyFetcherAPI
=======================

* Get list of dependencies for a url resource
* for each `url` source
    * if `html` -> list css, js, img (relative paths are returned as absolute)
    * if `json` -> crawl for any str that are absolute urls
* each url fetch is cached for 5 min

```bash
# brew install uv
./app.py


curl \
--request GET \
--url 'http://localhost:8000/dependenciesOf' \
--data-urlencode 'urls=https://www.bbc.co.uk/'


curl \
--request GET \
--url 'http://localhost:8000/dependenciesOf' \
--header 'Accept: application/vnd.global.22+json' \
--data-urlencode 'urls=https://bff-mobile-guacamole.musicradio.com/features/news/all-users'


curl \
--request POST \
--url 'http://localhost:8000/dependenciesOf' \
--header "Content-Type: application/json" \
--data '{"urls":[
"https://articles.globalplayer.com/7giJHKNG3vRYWz22MQDbr2cB15",
"https://articles.globalplayer.com/7giKbKdgfzZKpCuxeZoboczrJR",
"https://articles.globalplayer.com/2GXq7YzGSto2e4YSwMKe1E4Axsn",
"https://articles.globalplayer.com/2GXq9tnYwd3gFxGwkduSByRU8vK",
"https://articles.globalplayer.com/2GXqAi1GFY3EVxpuzeVtyvvB3kr",
"https://articles.globalplayer.com/2GXqCJ8ecdDpCoBgJLP8EzcVECu",
"https://articles.globalplayer.com/2GXqA1rS48FHjB3JKpjRXVvc3X8",
"https://articles.globalplayer.com/2GXqCcRs8jtHayMBYDMZMQMaHnG"
]}'


curl \
--url 'https://bff-mobile-guacamole.musicradio.com/features/news/all-users' \
--header 'Accept: application/vnd.global.22+json' \
| jq '.items[].items | .[]?.link.href' --raw-output

```


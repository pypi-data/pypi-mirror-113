# Overview
 Fetch a header info from header tag in HTML file. This package is in development. It only correspond to title tag.
 It returns a json object like this.
```
{
    'status': '<status>',
    'message': '<message>',
    'title': '<title>',
    'query': '<query>'
}
```
for example a successful case will be
```
{
    'status': 'OK',
    'message': 'fetching title success.',
    'title': 'Example Domain',
    'query': 'https://example.com'
}
```
and a bad case will be
```
{
    'status': 'ERR',
    'message': 'Invalid URL 'example.com': No schema supplied. Perhaps you meant http://example.com?',
    'title': None,
    'query': 'example.com'
}
```
The bad case returns an error code because the query is 'example.com', you should type 'https://example.com'.
# Usage
```py
from fetch_info import fetch_header

url = 'https://example.com'
fetch_header.fetch_title(url)
```


This software is released under the MIT License, see LICENSE.
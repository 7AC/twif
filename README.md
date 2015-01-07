twif
====
A wrapper around [TwitterSearch](https://github.com/ckoepp/TwitterSearch) and [pync](https://github.com/SeTeM/pync) to send recent search results from Twitter to Notification Center.

```
usage: twif.py [-h] --consumer-key CONSUMER_KEY --consumer-secret
               CONSUMER_SECRET --access-token ACCESS_TOKEN
               --access-token-secret ACCESS_TOKEN_SECRET [-d] [-k KEYWORD]
               [-v]
               KEYWORDS [KEYWORDS ...]

positional arguments:
  KEYWORDS              search keywords

optional arguments:
  -h, --help            show this help message and exit
  --consumer-key CONSUMER_KEY
                        Twitter API consumer key
  --consumer-secret CONSUMER_SECRET
                        Twitter API consumer secret
  --access-token ACCESS_TOKEN
                        Twitter API access token
  --access-token-secret ACCESS_TOKEN_SECRET
                        Twitter API access token secret
  -d, --debug           debug mode
  -k KEYWORD, --keyword KEYWORD
                        keyword to search
  -v, --verbose         verbose mode
```

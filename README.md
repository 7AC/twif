twif
====
A wrapper around [TwitterSearch](https://github.com/ckoepp/TwitterSearch) and [pync](https://github.com/SeTeM/pync) to send recent search results from Twitter to Notification Center.

```
usage: twif.py [-h] --consumer-key CONSUMER_KEY --consumer-secret
               CONSUMER_SECRET --access-token ACCESS_TOKEN
               --access-token-secret ACCESS_TOKEN_SECRET [-v]
               KEYWORD [KEYWORD ...]

positional arguments:
  KEYWORD               search keyword

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
  -v, --verbose         verbose mode
```

Sample usage:
```
twif.py --consumer-key aaabbb --consumer-secret cccddd \

        --access-token 111222 --access-token-secret 333444 \

        \$TWTR
```

results in:

![preview](preview.png)

Stick that in a `cron` job and you're done!

You can also blacklist users by adding them to `~/.twif/blacklist`.

To obtain a key and token to access the Twitter API you need to register at [apps.twitter.com](https://apps.twitter.com).

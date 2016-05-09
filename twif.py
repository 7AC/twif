#!/usr/bin/env python

''' Posts Twitter search results to Notification Center '''

import argparse
from datetime import datetime
import os
import sys
from pync import Notifier
from TwitterSearch import TwitterSearch, TwitterSearchOrder
from TwitterSearch.TwitterSearchException import TwitterSearchException
import requests

TWIF_DIR = os.path.expanduser('~') + '/.twif/'
HISTORY_FILE = TWIF_DIR + 'history'
BLACKLIST_FILE = TWIF_DIR + 'blacklist'

def strptime(timestamp):
    '''Parse timestamps in the format used by Twitter'''
    return datetime.strptime(timestamp, '%a %b %d %H:%M:%S +0000 %Y')

def search(twitter_search, keywords, verbose=False, debug=False, reset=False):
    '''Search for the specified keywords and notify'''
    # pylint: disable=too-many-locals
    tso = TwitterSearchOrder()
    tso.set_keywords(keywords)
    tso.set_include_entities(False)
    title = ' '.join(keywords)
    last_tweet_date = datetime.min
    if not os.path.exists(TWIF_DIR):
        os.mkdir(TWIF_DIR)
    # Read context
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE) as history:
            last_tweet_date = strptime(history.read())
    blacklist = []
    if os.path.exists(BLACKLIST_FILE):
        with open(BLACKLIST_FILE) as blacklist:
            blacklist = [user for user in blacklist \
                              if user.startswith('@')]
    last_new_tweet_date = datetime.min
    last_new_tweet_date_str = None
    for tweet in twitter_search.search_tweets_iterable(tso):
        date_str = tweet['created_at']
        date = strptime(date_str)
        if debug or date > last_tweet_date:
            if date > last_new_tweet_date:
                last_new_tweet_date = date
                last_new_tweet_date_str = date_str
            if reset:
                continue
            tid = tweet['id']
            screen_name = tweet['user']['screen_name']
            if '@' + screen_name in blacklist:
                continue
            # Convert to ASCII for Notifier
            text = tweet['text'].encode('ascii', 'ignore')
            url = 'http://twitter.com/%s/status/%d' % (screen_name, tid)
            Notifier.notify(text, title=title, subtitle='@%s' % screen_name,
                            sender='com.twitter.twitter-mac',
                            activate='com.apple.Safari', open=url)
            if verbose:
                print '@%s:' % screen_name, text
    # Write context
    if not debug and last_new_tweet_date_str:
        with open(HISTORY_FILE, 'w') as history:
            history.write(last_new_tweet_date_str)

def main():
    ''' Parses command-line arguments '''
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', metavar='KEYWORD', nargs='+',
                        help='search keyword')
    parser.add_argument('--consumer-key', required=True,
                        help='Twitter API consumer key')
    parser.add_argument('--consumer-secret', required=True,
                        help='Twitter API consumer secret')
    parser.add_argument('--access-token', required=True,
                        help='Twitter API access token')
    parser.add_argument('--access-token-secret', required=True,
                        help='Twitter API access token secret')
    parser.add_argument('--reset', action='store_true',
                        help='Reset the timestamp and notify only about new tweets')
    parser.add_argument('-d', '--debug', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    args = parser.parse_args()

    try:
        twitter_search = TwitterSearch(
            consumer_key=args.consumer_key,
            consumer_secret=args.consumer_secret,
            access_token=args.access_token,
            access_token_secret=args.access_token_secret)
        search(twitter_search, args.keyword, verbose=args.verbose,
               debug=args.debug, reset=args.reset)
    except (requests.exceptions.ConnectionError,
            TwitterSearchException), exception:
        if args.verbose:
            print exception

if __name__ == "__main__":
    sys.exit(main())

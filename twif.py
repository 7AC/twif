#!/usr/bin/env python

from pync import Notifier
from TwitterSearch import TwitterSearch, TwitterSearchOrder
import argparse
from datetime import datetime

def search( ts, keywords, maxAge=600, debug=False ):
   tso = TwitterSearchOrder()
   tso.set_keywords( keywords )
   tso.set_include_entities( False )
   now = datetime.now()
   title = ' '.join( keywords )
   for tweet in ts.search_tweets_iterable( tso ):
      date = datetime.strptime( tweet[ 'created_at' ], '%a %b %d %H:%M:%S +0000 %Y' )
      delta = now - date
      if debug or ( not delta.days and delta.seconds <= maxAge ):
         tid = tweet[ 'id' ]
         screenName = tweet[ 'user' ][ 'screen_name' ]
         # @<name>: <text>, and ignore \u2026 in it
         text = ''.join( [ i if ord( i ) < 128 else '' for i in tweet[ 'text' ] ] )
         url = 'http://twitter.com/%s/status/%d' % ( screenName, tid )
         Notifier.notify( text, title=title, subtitle='@%s' % screenName,
                          sender='com.twitter.twitter-mac',
                          activate='com.apple.Safari', open=url )
         if debug:
            break

parser = argparse.ArgumentParser()
parser.add_argument( '--consumer-key', help='Twitter API consumer key' )
parser.add_argument( '--consumer-secret', help='Twitter API consumer secret' )
parser.add_argument( '--access-token', help='Twitter API access token' )
parser.add_argument( '--access-token-secret',
                     help='Twitter API access token secret' )
parser.add_argument( '-d', '--debug', action='store_true', help='debug mode' )
parser.add_argument( '-k', '--keyword', action='append', help='keyword to search' )
parser.add_argument( '-m', '--max-age', metavar='MINUTES', type=int, default=10,
                     help='maximum tweet age' )
args = parser.parse_args()

ts = TwitterSearch( consumer_key=args.consumer_key,
                    consumer_secret=args.consumer_secret,
                    access_token=args.access_token,
                    access_token_secret=args.access_token_secret )
search( ts, args.keyword, maxAge=args.max_age * 60, debug=args.debug )

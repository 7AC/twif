#!/usr/bin/env python

from pync import Notifier
from TwitterSearch import TwitterSearch, TwitterSearchOrder
import argparse
from datetime import datetime
import os
import requests

twifDir = os.path.expanduser( '~' ) + '/.twif/'
historyFile = twifDir + 'history'
blacklistFile = twifDir + 'blacklist'

def strptime( timestamp ):
   '''Parse timestamps in the format used by Twitter'''
   return datetime.strptime( timestamp, '%a %b %d %H:%M:%S +0000 %Y' )

def search( ts, keywords, verbose=False, debug=False ):
   '''Search for the specified keywords and notify'''
   tso = TwitterSearchOrder()
   tso.set_keywords( keywords )
   tso.set_include_entities( False )
   title = ' '.join( keywords )
   lastTweetDate = datetime.min
   if not os.path.exists( twifDir ):
      os.mkdir( twifDir )
   # Read context
   if os.path.exists( historyFile ):
      with open( historyFile ) as f:
         lastTweetDate = strptime( f.read() )
   blacklist = []
   if os.path.exists( blacklistFile ):
      with open( blacklistFile ) as f:
         blacklist = [ user for user in f.read().split( '\n' ) \
                            if user.startswith( '@' ) ]
   lastNewTweetDate = datetime.min
   lastNewTweetDateStr = None
   for tweet in ts.search_tweets_iterable( tso ):
      dateStr = tweet[ 'created_at' ]
      date = strptime( dateStr )
      if debug or date > lastTweetDate:
         if date > lastNewTweetDate:
            lastNewTweetDate = date
            lastNewTweetDateStr = dateStr
         tid = tweet[ 'id' ]
         screenName = tweet[ 'user' ][ 'screen_name' ]
         if '@' + screenName in blacklist:
            continue
         # Convert to ASCII for Notifier
         text = tweet[ 'text' ].encode( 'ascii', 'ignore' )
         url = 'http://twitter.com/%s/status/%d' % ( screenName, tid )
         Notifier.notify( text, title=title, subtitle='@%s' % screenName,
                          sender='com.twitter.twitter-mac',
                          activate='com.apple.Safari', open=url )
         if verbose:
            print '@%s:' % screenName, text
   # Write context
   if not debug and lastNewTweetDateStr:
      with open( historyFile, 'w' ) as f:
         f.write( lastNewTweetDateStr )

parser = argparse.ArgumentParser()
parser.add_argument( 'keyword', metavar='KEYWORD', nargs='+',
                     help='search keyword' )
parser.add_argument( '--consumer-key', required=True,
                     help='Twitter API consumer key' )
parser.add_argument( '--consumer-secret', required=True,
                     help='Twitter API consumer secret' )
parser.add_argument( '--access-token', required=True,
                     help='Twitter API access token' )
parser.add_argument( '--access-token-secret', required=True,
                     help='Twitter API access token secret' )
parser.add_argument( '-d', '--debug', action='store_true', help=argparse.SUPPRESS )
parser.add_argument( '-v', '--verbose', action='store_true', help='verbose mode' )
args = parser.parse_args()

try:
   ts = TwitterSearch( consumer_key=args.consumer_key,
                       consumer_secret=args.consumer_secret,
                       access_token=args.access_token,
                       access_token_secret=args.access_token_secret )
   search( ts, args.keyword, verbose=args.verbose, debug=args.debug )
except requests.exceptions.ConnectionError, e:
   if args.verbose:
      print e

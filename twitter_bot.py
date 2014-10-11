# -*- coding: utf-8 -*-
import twitter_functions as tf
from sys import platform as _platform

if _platform == 'linux' or _platform == 'linux2':
    # linux - AmazonEC2
    DATAPATH = '/home/ubuntu/twitter_bot/data/'
elif _platform == 'darwin':
    # OS X - Local
    DATAPATH = '/Users/WorkMachine/GDrive/DTU/socialGraphs/twitter_bot/data/'
elif _platform == 'win32':
    pass

JAMESLEE = tf.TwitterUser(
    CONSUMER_KEY='wj5GCsbfLi5hIJLfKPxLHuD4g',
    CONSUMER_SECRET='TQ7tp7QNr7VdnWhj1WxLLoEVqFBQWDbL9sgB9Ujy3YLvZi9O5H',
    OAUTH_TOKEN='2787540506-VF0mXfQ4CyWXvHv4pLGlV1z9eyCfUABJ8XRUh8b',
    OAUTH_TOKEN_SECRET='1uhfzNCJCVH06RVIo60sGu1h8ptZZD3BfCsN3R307f4yZ',
    path=DATAPATH,
    user_screen_name='canuckWong',
)

OLDED_THAN_TWEET = 518810391942819840
AMOUNT = 100
HASHTAGS = [
    'canucks',
    'vancouver',
    'hockey',
    'gastown',
    'whistler',
    'stanleypark',
    'englishbay',
    'sfu',
    'vancity',
    'raincouver',
    'yvr',
]

GEO_VANCOUVER = '49.28057636458604,-123.123702581543,10km'

HASHTAG_TWEETS = []
for i in enumerate(HASHTAGS):
    HASHTAG_TWEETS.append(JAMESLEE.twitter_api.search.tweets(q='#canucks',
                                                             count=AMOUNT,
                                                             max_id=OLDED_THAN_TWEET,
                                                             geocode=GEO_VANCOUVER))

# all_tweets = canucks + vancouver + hockey + gastown + whistler +
# stanleypark + englishbay + sfu + vancity + raincouver + yvr

# with open('hashTweets.json', 'w') as f:
# ....f.writelines(json.dumps(all_tweets, indent=4))

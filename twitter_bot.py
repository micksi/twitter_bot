import twitter, os, json
from twitter_functions import *

CONSUMER_KEY 		= 'wj5GCsbfLi5hIJLfKPxLHuD4g'
CONSUMER_SECRET 	= 'TQ7tp7QNr7VdnWhj1WxLLoEVqFBQWDbL9sgB9Ujy3YLvZi9O5H'
OAUTH_TOKEN 		= '2787540506-VF0mXfQ4CyWXvHv4pLGlV1z9eyCfUABJ8XRUh8b'
OAUTH_TOKEN_SECRET 	= '1uhfzNCJCVH06RVIo60sGu1h8ptZZD3BfCsN3R307f4yZ'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth = auth)

if os.path.isfile('all_tweets.json'):
	with open('all_tweets.json',mode = 'r') as f:
		old_tweets = json.load(f)
	tl = twitter_api.statuses.home_timeline(count = 200, since_id = old_tweets[0]['id'])
	writeToJSON(simplifyTwitterFeed(tl))
else:
	tl = twitter_api.statuses.home_timeline(count = 200)
	writeToJSON(simplifyTwitterFeed(tl))
import twitter, json, io

def simplifyTwitterFeed(tweetfeed):
	"""
	Formats a dictionary from twitter.statuses.home_timeline() to a smaller
	dictionary only including text, coordinates, retweet_count, id, created_at and
	user_id and returns the formatted dictionary.
	"""
	tweets = []
	for tweet in tweetfeed:
		tweets.append( {'text':tweet['text'],
						'coordinates':tweet['coordinates'],
						'retweet_count':tweet['retweet_count'],
						'id':tweet['id'],
						'created_at':tweet['created_at'],
						'user_id':tweet['user']['id']})
	return tweets

def writeToJSON(recent_tweets, path):
	""""
	Writes a dictionary to a file in JSON format and in unicode(utf-8).
	"""
	try:
		with open(path,mode = 'r') as f:
			old_tweets = json.load(f)

		_tweets = recent_tweets + old_tweets

		with open(path,mode = 'w') as f:
			json.dump(_tweets,f, indent=4)
	except IOError:
		with open(path,'w') as f:
			json.dump(recent_tweets,f,indent=4)
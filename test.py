import json
import twitter_bot as t

with open('data/tl_tweets.json',mode='r') as f:
	tweets = json.load(f)

print t.jamesLee._is_last_24h(tweets[500]['created_at'])

import twitter
import json
import re

from sys import platform as _platform

if _platform == 'linux' or _platform == 'linux2':
    # linux - AmazonEC2
    path = '/home/ubuntu/twitter_bot/handin2/'
elif _platform == 'darwin':
    # OS X - Local
    path = '/Users/mickneupart/gdrive/DTU/socialGraphs/handin2/'
elif _platform == 'win32':
    pass

def write_to_json(content, path):
    """"
........encoded in unicode(utf-8).
........"""

    try:
        with open(path + 'followers_friend_&_follower.json', mode='r') as f:
            old_content = json.load(f)

        total_content = content + old_content

        with open(path + 'followers_friend_&_follower.json', mode='w') as f:
            json.dump(total_content, f, indent=4)
    except IOError:
        print 'No file, creating one!'
        with open(path + 'followers_friend_&_follower.json', 'w') as f:
            json.dump(content, f, indent=4)

CONSUMER_KEY='wj5GCsbfLi5hIJLfKPxLHuD4g'
CONSUMER_SECRET='TQ7tp7QNr7VdnWhj1WxLLoEVqFBQWDbL9sgB9Ujy3YLvZi9O5H'
OAUTH_TOKEN='2787540506-VF0mXfQ4CyWXvHv4pLGlV1z9eyCfUABJ8XRUh8b'
OAUTH_TOKEN_SECRET='1uhfzNCJCVH06RVIo60sGu1h8ptZZD3BfCsN3R307f4yZ'

auth = twitter.oauth.OAuth(OAUTH_TOKEN,
                           OAUTH_TOKEN_SECRET, 
                           CONSUMER_KEY,
                           CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)
	
with open(path + 'not_tried_ids.txt', mode='r') as f:
	ids = [int(id) for id in f.readlines()]
	
	try:
		try_ids = ids[:5]
		remaining_ids = ids[5:]
	except IndexError:
		try_ids = ids
		remaining_ids = []

try:
	with open(path + 'followers_friend_&_follower.json', mode='r') as f:
		users = json.load(f)
except IOError:
	users = []


for id in try_ids:
	user_followers = twitter_api.followers.ids(user_id=id)
	user_friends = twitter_api.friends.ids(user_id=id)
	tmp = {'user_id':id, 
		   'followers':user_followers, 
		   'friends':user_friends}
	users.append(tmp)

with open(path + 'not_tried_ids.txt', mode='w') as f:
	[f.write(str(id) + '\n') for id in remaining_ids]

write_to_json(users, path)



# my_followers = twitter_api.followers.ids(user_name='wongytong')
# my_friends = twitter_api.friends.ids(user_name='wongytong')

# users = []
# users.append({'user_id':'wongytong', 
# 			  'followers_id':my_followers, 
# 			  'friends_id':my_friends})

# write_to_json(users, path)


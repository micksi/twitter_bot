import twitter_functions as tf

#AmazonEC2
#dataPath = '/home/ubuntu/twitter_bot/data/'

#Local
dataPath = '/Users/WorkMachine/GDrive/DTU/socialGraphs/twitter_bot/data/'

jamesLee = tf.TwitterUser(CONSUMER_KEY 			= 'wj5GCsbfLi5hIJLfKPxLHuD4g',
						  CONSUMER_SECRET 		= 'TQ7tp7QNr7VdnWhj1WxLLoEVqFBQWDbL9sgB9Ujy3YLvZi9O5H',
						  OAUTH_TOKEN 			= '2787540506-VF0mXfQ4CyWXvHv4pLGlV1z9eyCfUABJ8XRUh8b',
						  OAUTH_TOKEN_SECRET 	= '1uhfzNCJCVH06RVIo60sGu1h8ptZZD3BfCsN3R307f4yZ',
						  path 					= dataPath,
						  user_screen_name		= 'canuckWong')
1
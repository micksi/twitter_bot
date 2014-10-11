import twitter_functions as tf
from sys import platform as _platform

if _platform == "linux" or _platform == "linux2":
    # linux - AmazonEC2
    dataPath = '/home/ubuntu/twitter_bot/data/'
elif _platform == "darwin":
    # OS X - Local
    dataPath = '/Users/WorkMachine/GDrive/DTU/socialGraphs/twitter_bot/data/'
elif _platform == "win32":
    pass


jamesLee = tf.TwitterUser(CONSUMER_KEY='wj5GCsbfLi5hIJLfKPxLHuD4g',
                          CONSUMER_SECRET='TQ7tp7QNr7VdnWhj1WxLLoEVqFBQWDbL9sgB9Ujy3YLvZi9O5H',
                          OAUTH_TOKEN='2787540506-VF0mXfQ4CyWXvHv4pLGlV1z9eyCfUABJ8XRUh8b',
                          OAUTH_TOKEN_SECRET='1uhfzNCJCVH06RVIo60sGu1h8ptZZD3BfCsN3R307f4yZ',
                          path=dataPath,
                          user_screen_name='canuckWong')

jamesLee.save_latest_tweets()

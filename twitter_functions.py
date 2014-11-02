#!/usr/bin/python
# -*- coding: utf-8 -*-
import twitter
import json
import re
from datetime import datetime
from datetime import timedelta
import random
import youtube_extractor


class TwitterUser:

    """
....Class used to botify a twitter account.
....When declaring the path, use only a directory
....not already being used by another user.
...."""

    def __init__(
        self,
        CONSUMER_KEY,
        CONSUMER_SECRET,
        OAUTH_TOKEN,
        OAUTH_TOKEN_SECRET,
        path,
        user_screen_name,
    ):

        self.auth = twitter.oauth.OAuth(OAUTH_TOKEN,
                                        OAUTH_TOKEN_SECRET, CONSUMER_KEY,
                                        CONSUMER_SECRET)
        self.twitter_api = twitter.Twitter(auth=self.auth)
        self.path = path
        self.user_screen_name = user_screen_name

        # Files used to store tweets, ids, etc

        self.tried_txt = 'ids_tried_friends.txt'
        self.pending_txt = 'ids_pending_friendship.txt'
        self.tl_tweets_json = 'tl_tweets.json'

    # ---------------------------- ACTIONS ------------------------------....

    def save_latest_tweets(self):
        """
........Save the Lastest tweets from the auth timeline at the specified path.
........If no path exists create new else find the latest id and save the tweets
........from that time.
........"""

        try:
            with open(self.path + self.tl_tweets_json, mode='r') as f:
                old_tweets = json.load(f)

            tl = self.twitter_api.statuses.home_timeline(count=200,
                                                         since_id=old_tweets[0]['id'])
            self._write_to_json(self._simplify_twitter_feed(tl),
                                self.tl_tweets_json)
        except IOError:
            tl = self.twitter_api.statuses.home_timeline(count=200)
            self._write_to_json(self._simplify_twitter_feed(tl),
                                self.tl_tweets_json)

        # print "TWEETS - added: " + str(len(tl)) + " tweets to " +
        # self.tl_tweets_json

    def reciprocal_follow_start(self, search_text, geo=False):
        """
........Start the reciprocal follow routine
........Follow amount(2) if they don't follow back remove them from your friends.
........"""

        page_no = int(random.random() * 20 + 1)  # Max 50 pages
        p = self.twitter_api.users.search(q=search_text, count=20,
                                          page=page_no)

        # Follow bots
        p2f = []
        for person in p:
            for word in search_text:
                p2f.append(person['id'])
        
        self._save_id_list_to_file(self.pending_txt, content=p2f)
        self._follow_id(p2f)

        # Follow humans in SAN FRANCISCO
        SF_LAT = 37.753360
        SF_LONG = -122.480521
        radius = '50km'
        humans = twitter_api.search.tweets(geocode=area, lang='en', count=25)

        h2f2 = [status['user']['id'] for status in humans['statuses']
                    if (float(status['user']['friends_count'])/ \
                        status['user']['followers_count']) > 0.7]

        self._save_id_list_to_file(self.pending_txt, content=h2f2)
        self._follow_id(h2f2)

        print 'Reciprocal Follow is started'

    def reciprocal_follow_end(self):
        """
........End the reciprocal follow routine
........"""

        self._unfollow_no_friendship(file_=self.pending_txt)
        self._save_id_list_to_file(self.pending_txt, truncate=True)

        print 'End Reciprocal - unfollowing friends because they did not follow back'

    def tweet_most_retweeted_in_last_24h(self):
        """
........Tweet the most retweeted tweet in the last 24 hours from your own timeline
........"""

        with open(self.path + self.tl_tweets_json, mode='r') as f:
            tweets = json.load(f)

        last_24h_tweets = [tweet for tweet in tweets[:5000]
                           if self._is_last_24h(tweet['created_at'])
                           and tweet['retweet_count'] > 10]
        last_24h_retweet_count = [tweet['retweet_count'] for tweet in
                                  last_24h_tweets]

        max_retweet_index = \
            last_24h_retweet_count.index(max(last_24h_retweet_count))

        self.twitter_api.statuses.retweet(id=tweets[max_retweet_index]['id'])

        # self.twitter_api.statuses.retweet(id=519406310165839872)
        # print tweets[max_retweet_index]['id']

    def random_tweet(self):
        """
........Make a random tweet, yet to be implemented
........"""
        self.twitter_api.statuses.update(
                    status=youtube_extractor.get_tweet_text(),
                    lat=37.753360,
                    long=-122.480521,
                    display_coordinates=True)
        

# ---------------------------- TOOLS ------------------------------

    def _simplify_twitter_feed(self, tweetfeed):
        """
........Formats a dictionary from twitter.statuses.home_timeline() to a smaller
........dictionary only including text, coordinates, retweet_count, id, created_at and
........user_id and returns the formatted dictionary.
........"""

        tweets = []
        for tweet in tweetfeed:
            tweets.append({
                'text': tweet['text'],
                'coordinates': tweet['coordinates'],
                'retweet_count': tweet['retweet_count'],
                'id': tweet['id'],
                'created_at': tweet['created_at'],
                'user_id': tweet['user']['id'],
            })
        return tweets

    def _unfollow_id(self, user_id):
        """
........Can either parse a list or just a single int
........"""

        if type(user_id) == list:
            [self.twitter_api.friendships.destroy(user_id=id_)
             for id_ in user_id]
        elif type(user_id) == int:
            self.twitter_api.friendships.destroy(user_id=user_id)

    def _get_friends_id(self):
        """
........Gets a list of all those who you are following (friends) and returns a list with the ID's
........OBS! max 5000 friends is allowed, should probably be modified to allow for more friends.
........"""

        friends = \
            self.twitter_api.friends.ids(screen_name=self.user_screen_name,
                                         count=5000)
        return friends['ids']

    def _unfollow_no_friendship(self, all_friends=False, file_=None):
        """
........Unfollow whoever is not following you back, all_friends or a file containing ids.
........all_friends overwrites the specified file. File defaults to self.pending_txt!

........all_friends: Removes ALL who you are following and not following you back, BE CAREFUL!!!
........file: Removes friends who are in the specified file, defaults to the pending friendship requests.
........"""

        if file_ is None:
            file_ = self.pending_txt

        if all_friends is True:
            friends_id = self.get_friends_id_list()
            for id_ in friends_id:
                relation = \
                    self.twitter_api.friendships.show(source_screen_name=self.user_screen_name,
                                                      target_id=id_)
                if relation['relationship']['target']['following'] \
                        is False:
                    self._unfollow_id(id_)
        else:
            try:
                id_list = self._get_ids_list_from_file(file_)
                for id_ in id_list:
                    relation = \
                        self.twitter_api.friendships.show(source_screen_name=self.user_screen_name,
                                                          target_id=id_)
                    if relation['relationship']['target']['following'] \
                            is False:
                        self._unfollow_id(id_)
            except self.twitter_api.TwitterHTTPError:
                print 'Something went wrong when defriending!?'

    def _follow_id(self, follow_id):
        """
........Only follows if you're not already following.
........follow_id must be a int or list of ints!
........"""

        if type(follow_id) is not list:
            follow_id = [follow_id]

        try:
            if type(follow_id) is list:
                tried_list = \
                    self._get_ids_list_from_file(self.tried_txt)
                p_2_follow = [id_ for id_ in follow_id if id_
                              not in tried_list]

                [self.twitter_api.friendships.create(user_id=id_)
                 for id_ in p_2_follow]

                self._save_id_list_to_file(self.tried_txt,
                                           content=follow_id)
                print 'tried to friend: ' + str(len(p_2_follow)) \
                    + ' person(s). Total: ' + str(len(follow_id))
        except IOError:
            print 'the follow_id(s) provided is not of type(int)'

# ------------------------- to file writing stuff ----------------------

    def _get_ids_list_from_file(self, txt_file):
        try:
            with open(self.path + txt_file, mode='r') as f:
                lines = f.readlines()
                id_list = [int(line.strip()) for line in lines]
            return id_list
        except IOError:
            print 'No file to be found! at\n' + self.path \
                + '\nDoes the file exist?'
            return []

    def _write_to_json(self, content, json_file):
        """"
........encoded in unicode(utf-8).
........"""

        try:
            with open(self.path + json_file, mode='r') as f:
                old_content = json.load(f)

            total_content = content + old_content

            with open(self.path + json_file, mode='w') as f:
                json.dump(total_content, f, indent=4)
        except IOError:
            print 'No file, creating one!'
            with open(self.path + json_file, 'w') as f:
                json.dump(content, f, indent=4)

    def _is_last_24h(self, tweet_date):
        """
........The date have to be formatted as a single string:
........'day_name month_name day_no hours_no minutes_no seconds_no random_no year_no'
........"""

        present = datetime.now()
        tweet_date = str(tweet_date)
        if present - self._convert_tweet_date_to_datetime(tweet_date) \
                < timedelta(hours=24):
            return True
        else:
            return False

    def _convert_tweet_date_to_datetime(self, tweet_date):
        """
........Converts the twitter field 'created_at' into datetime format
........"""

        months = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12,
        }
        date = re.split(':| ', tweet_date)
        year = int(date[7])
        month = int(months[date[1]])
        day = int(date[2])
        hour = int(date[3])
        minute = int(date[4])
        second = int(date[5])

        return datetime(
            year,
            month,
            day,
            hour,
            minute,
            second,
        )

    def _save_id_list_to_file(
        self,
        txt_file,
        content=None,
        truncate=False,
    ):
        """
........OBS! auto converts the content to type str before saving
........"""

        if truncate is True:
            with open(self.path + txt_file, mode='w') as f:
                pass
            print 'deleting content in: ' + txt_file + '!'
            return

        if type(content) != list:
            content = [content]

        try:
            with open(self.path + txt_file, mode='r') as f:
                old_content = [line for line in f if line.strip()]
                new_content = [str(e) + '\n' for e in content]
                total_content = old_content + new_content

            with open(self.path + txt_file, mode='w') as f:
                [f.write(line) for line in total_content]
        except IOError:
            print 'No file, creating one!'
            with open(self.path + txt_file, mode='w') as f:
                total_content = [str(e) + '\n' for e in content]
                [f.write(line) for line in total_content]

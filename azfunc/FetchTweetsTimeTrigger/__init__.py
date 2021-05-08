import logging
import azure.functions as func
import typing
import time
import datetime
import os
import requests
import json


class Tweet(object):
    """Tweet object:
    self.text (str): content of the tweet
    self.hashtags (lst(str)): list of hashtags in the tweet
    self.time (str): timestamp of when the tweet was posted
    self.user_id (str): the Twitter user_id of the poster
    """

    # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
    def __init__(self, raw_tweet=None, tweet_to_copy=None):
        if raw_tweet != None:
            text, hashtags, hashtag, time, user_id, tweet_id = self._parse(
                raw_tweet)
            self.id = tweet_id
            self.text = text
            self.hashtags = hashtags
            self.hashtag = hashtag  # first of hashtags
            self.time = time
            self.user_id = user_id
        elif tweet_to_copy != None:
            self.id = tweet_to_copy.id
            self.text = tweet_to_copy.text
            self.hashtags = tweet_to_copy.hashtags
            self.hashtag = tweet_to_copy.hashtag
            self.time = tweet_to_copy.time
            self.user_id = tweet_to_copy.user_id

    def _parse(self, raw_tweet):
        """Private method. Outputs tuple of (text, hashtags, time, user_id)"""
        # formats it into the fields we want. Check example json.
        text = raw_tweet['data']['text']
        if type(text) != str:
            text = text.decode()
        hashtags = []
        if 'entities' in raw_tweet['data'] and 'hashtags' in raw_tweet['data']['entities']:
            hashtags = [x['tag']
                        for x in raw_tweet['data']['entities']['hashtags']]
        hashtag = hashtags[0] if (
            len(hashtags) > 0) else ""
        time = raw_tweet['data']['created_at']
        user_id = raw_tweet['data']['author_id']
        tweet_id = raw_tweet['data']['id']

        return text, hashtags, hashtag, time, user_id, tweet_id

    def set_hashtag(self, hashtag):
        self.hashtag = hashtag

    def set_id(self, tweet_id):
        self.id = tweet_id

    def copy_with_hashtag(self, hashtag, append_at_tweet_id=""):
        copied = Tweet(tweet_to_copy=self)
        copied.set_hashtag(hashtag)
        copied.set_id(self.id + append_at_tweet_id)
        return copied

    def split_with_hashtags(self):
        """ Returns a list of Tweets with one hashtag each from self.
            If self has no hashtag, an empty list is returned. """
        tweets = [self.copy_with_hashtag(hashtag, append_at_tweet_id=str(
            idx)) for idx, hashtag in enumerate(self.hashtags)]
        return tweets

    def format_db_entry(self):
        """Public function. Will make Tweet object into form of db entry. @TODO decide on exactly what that is"""
        pass


def get_tweets(end_time):
    """
    Get 1% of raw tweets in stream from twitter api. Will function as connection method.
    Runs until end_time.
    """
    headers = {'Authorization': 'Bearer {}'.format(
        os.environ.get("BEARER_TOKEN"))}
    url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=author_id,created_at,entities"
    response = requests.request('GET', url, headers=headers, stream=True)
    tweets = []
    print(response.status_code)
    if response.status_code != 200:
        print(response.text)
        return
    for response_line in response.iter_lines():
        if time.time() > end_time:
            break
        if response_line:
            json_response = json.loads(response_line)
            new_tweet = Tweet(raw_tweet=json_response)
            new_tweets = new_tweet.split_with_hashtags()
            tweets.extend(new_tweets)
    return tweets


def main(msg: func.Out[typing.List[str]], mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    end_time = time.time() + 5
    tweets = get_tweets(end_time)
    qtweets = [json.dumps(tweet.__dict__) for tweet in tweets]
    msg.set(qtweets)

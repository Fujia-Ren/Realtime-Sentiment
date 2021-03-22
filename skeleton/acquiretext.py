import requests
import os
import json


#in terminal, export "BEARER_TOKEN=<bearer_token>"

class Tweet(object):
    """Tweet object:
    self.text (str): content of the tweet
    self.hashtags (lst(str)): list of hashtags in the tweet
    self.time (str): timestamp of when the tweet was posted
    self.user_id (str): the Twitter user_id of the poster	
    """

    # https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
    def __init__(self, raw_tweet):
        text, hashtags, time, user_id = self._parse(raw_tweet)
        self.text = text
        self.hashtags = hashtags
        self.time = time
        self.user_id = user_id

    def _parse(self, raw_tweet):
        """Private method. Outputs tuple of (text, hashtags, time, user_id)"""
        # formats it into the fields we want. Check example json.
        text = raw_tweet['data']['text']
        hashtags = []
        if 'entities' in raw_tweet['data'] and 'hashtags' in raw_tweet['data']['entities']:
            hashtags = [x['tag'] for x in raw_tweet['data']['entities']['hashtags']]
        time = raw_tweet['data']['created_at']
        user_id = raw_tweet['data']['author_id']

        return text, hashtags, time, user_id

    def format_db_entry(self):
        """Public function. Will make Tweet object into form of db entry. @TODO decide on exactly what that is"""
        pass 

def get_tweets():
    """
    Get 1% of raw tweets in stream from twitter api. Will function as connection method.
    """
    headers = {'Authorization': 'Bearer {}'.format(os.environ.get("BEARER_TOKEN"))}
    url = "https://api.twitter.com/2/tweets/sample/stream?tweet.fields=author_id,created_at,entities"
    response = requests.request('GET', url, headers=headers, stream=True)
    tweets = []
    print(response.status_code)
    if response.status_code != 200:
        print(response.text)
        return
    for response_line in response.iter_lines():
        if response_line:
            json_response = json.loads(response_line)
            new_tweet = Tweet(json_response)
            tweets.append(new_tweet)
            print(new_tweet.user_id)
            print(new_tweet.time)
            print(new_tweet.text)
            print(new_tweet.hashtags)
            #print(json.dumps(json_response, indent=4, sort_keys=True))


def send_to_db(texts):
    """
      db means cosmos db (TEXT DB)
      texts is list of texts (could be a single text, really doesn't matter)
      input the texts into the TEXT DB
    """


if __name__ == "__main__":

        # For every min/hour/day (doesn't matter)
    get_tweets()
        # for tweet in tweets:
        #     #note that tweet is a Tweet object
        #     send_to_db(tweet.format_db_entry())
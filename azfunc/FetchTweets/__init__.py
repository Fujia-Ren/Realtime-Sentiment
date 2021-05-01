import logging
import azure.functions as func
import time
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

def get_tweets(end_time):
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
        if time.time() > end_time:
            break
        if response_line:
            json_response = json.loads(response_line)
            new_tweet = Tweet(json_response)
            if type(new_tweet.text) != str:
                new_tweet.text = new_tweet.text.decode()
            tweets.append(new_tweet)
    return tweets

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    end_time = time.time() + 5
    tweets = get_tweets(end_time)
    response_body = json.dumps([tweet.__dict__ for tweet in tweets])

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    

    if name:
        return func.HttpResponse(response_body, status_code=200)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

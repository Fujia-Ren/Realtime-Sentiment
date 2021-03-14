class Tweet(object):
	"""Tweet object:
	self.text (str): content of the tweet
	self.hashtags (lst(str)): list of hashtags in the tweet
	self.time (str): timestamp of when the tweet was posted
	self.user_id (str): the Twitter user_id of the poster	
	"""

	#https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet
	def __init__(self, raw_tweet):
		text, hashtags, time, user_id = self._format(raw_tweet)
		self.text = text
		self.hashtags = hashtags
		self.time = time
		self.user_id = user_id

	def _format(self, raw_tweet):
		"""Private method. Outputs tuple of (text, hashtags, time, user_id)"""
		#formats it into the fields we want. Check example json. 

def get_tweets():
    """
    get_text from the twitch api
    """
    # example = [
    #     {
    #         "text": "Look at our planet earth",
    #         "hashtags": ["earth", "life"],
    #         "time": 2020,
    #         "user_id": "globelover"
    #     },
    #     {
    #         "text": "Qb4 Yay",
    #         "hashtags": ["chess", "gm"],
    #         "time": 2019,
    #         "user_id": "chesscracker"
    #     }
    # ]
	

	##Connect to Twitter in stream. 
	for raw_tweet in stream:
		new_tweet = Tweet(raw_tweet)
		example.append(raw_tweet)
	return example


def send_to_db(texts):
    """
      db means cosmos db (TEXT DB)
      texts is list of texts (could be a single text, really doesn't matter)
      input the texts into the TEXT DB
    """


if __name__ == "__main__":

	while(True):
		# For every min/hour/day (doesn't matter)
		tweets = get_tweets()
		for tweet in tweets:
			send_to_db(tweet.text)

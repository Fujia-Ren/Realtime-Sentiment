

def get_tweets():
    """
      get_text from the twitch api
    """
    example = [
        {
            "text": "Look at our planet earth",
            "hashtags": ["earth", "life"],
            "time": 2020,
            "user_id": "globelover"
        },
        {
            "text": "Qb4 Yay",
            "hashtags": ["chess", "gm"],
            "time": 2019,
            "user_id": "chesscracker"
        }
    ]
    return example


def extract_texts(tweets):
    """
      extract texts from the tweets, in the text form we use for our CosmosDB
      TEXT DATA FORM SHOULD BE CONSISTENT WITH analyzetext.py
    """
    placeholder = ""
    return placeholder


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
        texts = extract_texts(tweets)
        send_to_db(texts)

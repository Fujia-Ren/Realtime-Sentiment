import logging
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import azure.functions as func


def average(sentiment, avg, frequency):
    for field, score in avg.items():
        newScore = sentiment[field]
        avg[field] = ((frequency-1)*score + newScore)/frequency
    return avg


def main(msgIn: func.QueueMessage, currentDoc: func.DocumentList, newDoc: func.Out[func.Document]):
    # currentDisplayDoc: func.DocumentList, newDisplayDoc: func.Out[func.Document]):
    #logging.info('Python queue trigger function processed a queue item.')
    # get the tweet
    msg_body = msgIn.get_body().decode('utf-8')
    # print(msg_body)
    # print(type(msg_body))
    # .decode('utf-8')
    msg_dict = json.loads(msg_body)
    tweet = msg_dict['text']
    hashtag = msg_dict['hashtag'] if (
        msg_dict['hashtag'] != "") else "NOHASHTAG"
    #hashtags = msg_dict['hashtag']

    # analyze the sentiment of the tweet
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(tweet)

    # if the hashtag is not in the DB, add a new record
    if len(currentDoc) == 0:
        logging.info(f'new entry for {hashtag} with tweet {tweet}')

        newData = func.Document.from_dict({
            'id': hashtag,
            'sentiment': json.dumps(scores),
            'frequency': 1,
            'tweets': [tweet]
        })
        newDoc.set(newData)

    # if the hashtag is in the DB, update the entry:
    # - increment the frequency
    # - add the sentiment for this tweet to the running average
    # - add the tweet to the list of sample tweets
    else:
        old_data = currentDoc[0]

        # increment frequency
        frequency = old_data['frequency'] + 1

        # update sentiment
        running_avg = json.loads(old_data['sentiment'])
        new_avg = average(scores, running_avg, old_data['frequency'] + 1)
        if 'tweets' in old_data:
            tweets = old_data['tweets']
        else:
            tweets = []

        # update sample tweets
        tweets.append(tweet)
        if len(tweets) > 10:
            tweets.pop(0)

        logging.info(f'updated info for {hashtag} with tweets {tweets}')

        newData = func.Document.from_dict({
            'id': hashtag,
            'frequency': frequency,
            'sentiment': json.dumps(new_avg),
            'tweets': tweets
        })
        newDoc.set(newData)

    """
    # Update count in the displayDB
    if len(currentDisplayDoc) != 0:
        old_count_data = currentDisplayDoc[0]
        new_count = old_count_data['count'] + 1
        newDisplayData = func.Document.from_dict({
            'id': "count",
            'count': new_count
        })
        newDisplayDoc.set(newDisplayData)
        """

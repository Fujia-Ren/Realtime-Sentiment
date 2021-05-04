import logging
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

import azure.functions as func


def average(sentiment, avg, count):
    for field, score in avg.items():
        newScore = sentiment[field]
        avg[field] = ((count-1)*score + newScore)/count
    return avg


def main(msgIn: func.QueueMessage, currentDoc: func.DocumentList, newDoc: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python queue trigger function processed a queue item.')
    # get the tweet
    msg_body = msgIn.get_body().decode('utf-8')
    print(msg_body)
    print(type(msg_body))
    # .decode('utf-8')
    msg_dict = json.loads(msg_body)
    tweet = msg_dict['text']
    hashtag = msg_dict['hashtags'][0] if (
        len(msg_dict['hashtags']) > 0) else "NOHASHTAG"
    #hashtags = msg_dict['hashtag']

    # analyze the sentiment of the tweet
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(tweet)

    # if the hashtag is not in the DB, add a new record
    if len(currentDoc) == 0:
        newData = func.Document.from_dict({
            'id': hashtag,
            'sentiment': json.dumps(scores),
            'count': 1
        })
        newDoc.set(newData)
        return func.HttpResponse('wrote new data')

    # if the hashtag is in the DB, increment the count and add the sentiment
    # for this tweet to the running average
    else:
        oldData = currentDoc[0]
        running_avg = json.loads(oldData['sentiment'])
        new_avg = average(scores, running_avg, oldData['count'] + 1)
        newData = func.Document.from_dict({
            'id': hashtag,
            'sentiment': json.dumps(new_avg),
            'count': oldData['count'] + 1
        })
        newDoc.set(newData)
        return func.HttpResponse('updated old data')


"""
TODO:
- handle the case where there are multiple hashtags
- possibly change trigger to queue
- handle concurrency control (multiple functions writing to the same row)
- sample input: { "text": "hello world", "hashtag": "tag" }
"""

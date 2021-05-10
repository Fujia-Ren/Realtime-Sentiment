import azure.functions as func
import logging
import json


def main(documents: func.DocumentList, currentFrequencies: func.DocumentList, newFrequencies: func.Out[func.Document]):
    logging.info(f'{len(documents)} hashtags updated')
    frequent_hashtags = []

    # case 1: already have a frequency list in display db
    if currentFrequencies:
        frequencies_dict = json.loads(currentFrequencies[0].to_json())
        current_frequent_hashtags = frequencies_dict['hashtags']

        # initialize list of frequent hashtags with current list
        frequent_hashtags = current_frequent_hashtags
        logging.info('old frequent hashtags')
        logging.info([(tag['id'], tag['frequency']) for tag in frequent_hashtags])

        # iterate through updated entries in hashtags db to see if they should be added to the list
        # invariant: frequent_hashtags has the 10 most frequent hashtags sorted in descending order
        for document in documents:
            hashtag_data = json.loads(document.to_json())

            # add to the list if:
            # - current list length is < 10
            # - or this hashtag has a higher frequency than the last entry in the (sorted) list
            if len(frequent_hashtags) < 10 or (hashtag_data['frequency'] >= frequent_hashtags[-1]['frequency']):
                # if there is already an entry for this hashtag, remove it 
                # (will be replaced with new entry)
                hashtag_to_remove = None
                for current_hashtag in frequent_hashtags:
                    if current_hashtag['id'] == hashtag_data['id']:
                        hashtag_to_remove = current_hashtag
                if hashtag_to_remove:
                    frequent_hashtags.remove(hashtag_to_remove)

                # add the new data to the list
                frequent_hashtags.append(hashtag_data)

                # sort list in descending order and cut off after first 10 entries
                frequent_hashtags.sort(key=lambda x: x['frequency'], reverse=True)
                frequent_hashtags = frequent_hashtags[:10]
    
    # case 2: no frequency list in the display db
    # take 10 most frequent hashtags from the updated entries in hashtags db
    else:
        frequent_hashtags = [json.loads(document.to_json()) for document in documents]
        frequent_hashtags.sort(key=lambda x: x['frequency'], reverse=True)
        frequent_hashtags = frequent_hashtags[:10]
    
    # update the display db with the most frequent hashtags, as calculated above
    logging.info('new frequent hashtags')
    logging.info([(tag['id'], tag['frequency']) for tag in frequent_hashtags])
    newData = func.Document.from_dict({'id': 'display_frequent', 'hashtags': frequent_hashtags})
    newFrequencies.set(newData)
    

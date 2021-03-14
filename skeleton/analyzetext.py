

def get_texts_from_db():
    """
      db means cosmos db (TEXT DB).
      extract texts from the tweets, in the text form we use for our CosmosDB
      TEXT DATA FORM SHOULD BE CONSISTENT WITH analyzetext.py
    """

    example = [
        {
            "text": "I love chess",
            "hashtags": ["chess", "gm"]
        },
        {
            "text": "I love earth",
            "hashtags": ["earth", "dirt"]
        }
    ]
    return example


def make_document(texts_lst):
    """ 
        Make texts into a document to send to ML API
        Mainly to save price - ask Jenny for detail (google API)
    """
    document = ""
    for text in texts_lst:
        document += text
    return document


def send_analysis(doc):
    """
        To the ML API
    """
    analysis_result = ""
    return analysis_result


def update_hashtags(analysis):
    """
        With the analysis, update the data in HASHTAG DB accordingly 
    """
    pass


if __name__ == "__main__":
    while(True):
        # For every min/hour/day (doesn't matter)
        texts = get_texts_from_db()
        doc = make_document(texts)  # To send to
        analysis = send_analysis(doc)
        update_hashtags(analysis)

import azure.functions as func
import logging
import json


def main(documents: func.DocumentList, currentCount: func.DocumentList, newCount: func.Out[func.Document]):
    logging.info("count updat started")
    count = currentCount[0]["$1"]
    newData = func.Document.from_dict(
        {'id': 'count', 'count': count})
    newCount.set(newData)

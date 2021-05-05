import logging

import azure.functions as func


def main(msg: func.QueueMessage, newDoc: func.Out[func.Document]) -> None:
    logging.info('Python queue trigger function processed a queue item: %s',
                 msg.get_body().decode('utf-8'))
    msg_body = msg.get_body().decode('utf-8')
    data = func.Document.from_json(msg_body)
    newDoc.set(data)

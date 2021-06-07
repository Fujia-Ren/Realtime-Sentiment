import logging
import json
import azure.functions as func


def main(req: func.HttpRequest, currentDoc: func.DocumentList) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # distinguish between the types of queries. For now, only the basic frequency query is implemented.
    #request_type = req.params.get('type')
    request_id = req.params.get('id')
    if not request_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            #request_type = req_body.get('type')
            request_id = req_body.get('id')

    # add more cases here for other queries
    # id = "display_frequent"  # REMOVED
    # if request_type:  # REMOVED
    if request_id == "display_frequent":
        print('here')
        data = currentDoc[0]['hashtags']
        for elem in data:
            elem['sentiment'] = round(
                float(json.loads(elem['sentiment'])['compound']), 2)
        data_as_json = json.dumps(data)
        return func.HttpResponse(data_as_json)
    elif request_id == "count":
        data = currentDoc[0]['count']
        print(data)
        data_as_json = json.dumps(data)
        return func.HttpResponse(data_as_json)
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
            status_code=200
        )

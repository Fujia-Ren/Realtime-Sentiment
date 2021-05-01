import logging
import uuid

import azure.functions as func


def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        newdocs = func.DocumentList()
        newproduct_dict = {
            "id": str(uuid.uuid4()),
            "name": name
        }
        newdocs.append(func.Document.from_dict(newproduct_dict))
        doc.set(newdocs)
        return func.HttpResponse(f"Hello {name}!")
    else:
        return func.HttpResponse(
            "Please pass a name on the query string or in the request body",
            status_code=400
        )

import requests
import json
from requests.exceptions import HTTPError
from Wysebee import singleton

def raise_detailed_error(request_object):
    try:
        request_object.raise_for_status()
    except HTTPError as e:
        # raise detailed error message
        # TODO: Check if we get a { "error" : "Permission denied." } and handle automatically
        raise HTTPError(e, request_object.text)

@singleton
class Api:
    def __init__(self):
      pass

    def get_todos(self):
        request_ref = "https://jsonplaceholder.typicode.com/todos/"
        headers = {"content-type": "application/json; charset=UTF-8"}
        response = requests.get(request_ref, headers=headers)
        raise_detailed_error(response)
        return response.json()

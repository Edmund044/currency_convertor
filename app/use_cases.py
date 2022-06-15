import requests
from flask import jsonify
import json


def make_request_to_convert_currency(amount1,  currency1, currency2):
    url = "https://api.apilayer.com/fixer/convert?to=" + \
        currency2+"&from="+currency1+"&amount="+amount1

    payload = {}
    headers = {
        "apikey": "Slyih31Y8eUs3dRJgZyPjaPCzVh8s01y"
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    status_code = response.status_code
    res = json.loads(response.text)

    return res

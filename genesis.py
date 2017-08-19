#!/usr/bin/env python2.7

import json
import requests
from pprint import pprint
from pymongo import MongoClient


client = MongoClient()

db = client['bittrex']

collections = db['marketSummaries']

url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'

response = requests.get(url)
data = response.json()
#pprint (data)

doc_id = collections.insert_one(data).inserted_id
print doc_id

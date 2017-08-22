#!/usr/bin/env python2.7

import json
import requests
from pprint import pprint
from pymongo import MongoClient

client = MongoClient()

db = client['bittrex']

collections = db['marketSummaries']

url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
counter = 1
while True:
	response = requests.get(url)
	json_data = json.loads(response.text)
	responseList = json_data["result"]
	howLong =  len(responseList)
	counterI = 0
	while counterI < howLong - 1 :
        	counterI = counterI + 1
		collections.update(responseList[counterI], responseList[counterI], upsert=True)
		counter = counter + 1
		print counter


	print


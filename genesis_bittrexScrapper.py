#!/usr/bin/env python2.7

import json
import requests
from pprint import pprint
from pymongo import MongoClient
import pymongo
from time import sleep


client = MongoClient()

db = client['bittrex']

collections = db['marketSummaries']

url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
counter = 1
while True:
	response = requests.get(url)
	#data = response.json()
	json_data = json.loads(response.text)
	responseList = json_data["result"]
	howLong =  len(responseList)
	#print howLong
	counterI = 0
	while counterI < howLong - 1 :
        	counterI = counterI + 1
		#doc_id = collections.insert_one(responseList[counterI]).inserted_id
		#db.collections.update({noExist: true}, {"$setOnInsert": responseList[counterI]}, upsert=True)
		collections.update(responseList[counterI], responseList[counterI], upsert=True)
		#cursor = collections.find(responseList[counterI]).upsert().update_one({"$setOnInsert": responseList[counterI],"$set": {}})
		#print doc_id
		counter = counter + 1
		print counter

#	print "TEST IS IT HERE"
	print
#	sleep(.05)

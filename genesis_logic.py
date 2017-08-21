#!/usr/bin/env python2.7

import json
import requests
from pprint import pprint
from pymongo import MongoClient
from time import sleep

#Function that returns a list[ask, time, market] of the last NUMBER of samples for MARKET where the first element in the list is the latest data point and the last element in the list is the oldest datapoint. All elements in list are unique
def printLastNumbers( market , number):
	myGraphList = []
	cursor = collections.find({"MarketName": market }).sort("TimeStamp", -1)
	for document in cursor:
		#pprint(document['Ask'])
		#pprint(document['TimeStamp'])
		#pprint(document['MarketName'])
		myGraphList.append([document['Ask'],document['TimeStamp'],document['MarketName']])
		#mySetTemp = set(myGraphList)
		myGraphList = [list(t) for t in set(tuple(element) for element in myGraphList)]
		#number = number - 1
		if (number == len(myGraphList)):
			myGraphList = sorted(myGraphList,key=lambda l:l[1], reverse=True)
			return myGraphList
		#print '-----------------------------------------------------------------------------------------------------------------------------------------------'

#Function that will return a list of the different markets
def getMarkets():
	url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
	myMarketList = []
	counter = 1
	response = requests.get(url)
	json_data = json.loads(response.text)
	responseList = json_data["result"]
	howLong =  len(responseList)
	counterI = 0
	while counterI < howLong - 1 :
		counterI = counterI + 1
		#pprint(responseList[counterI]['MarketName'])
		myMarketList.append(responseList[counterI]['MarketName'])
		#print "______________________________________________________________________________________________________________________________________________________"
	return myMarketList

#Establishing connection to MongoDB database
client = MongoClient(host=['192.168.1.198:27017'])
#client = MongoClient(host=['108.196.157.14:27017'])

db = client['bittrex']

collections = db['marketSummaries']
# Connection Established


#printLastNumbers( "BTC-LSK" , 50)
#pprint(getMarkets())
#print getMarkets()

pprint(printLastNumbers("BTC-ETH", 100))
#for x in getMarkets():
#	pprint(printLastNumbers( x , 10))
#	print "______________________________________________________________________________________________________________________________________________________"
#	print "______________________________________________________________________________________________________________________________________________________"
#	print "______________________________________________________________________________________________________________________________________________________"

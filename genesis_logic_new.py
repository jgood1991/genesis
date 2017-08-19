#!/usr/bin/env python2.7

import json
import requests
from pprint import pprint
from pymongo import MongoClient
from time import sleep

def printLastNumber(cursor , number):
        for document in cursor:
                pprint(document)
                number = number - 1
                print number
                if (number == 0):
                        print "IS THIS WORKING"
                        return
                print '-----------------------------------------------------------------------------------------------------------------------------------------------'

client = MongoClient(host=['192.168.1.198:27017'])
#client = MongoClient(host=['108.196.157.14:27017'])

db = client['bittrex']

collections = db['marketSummaries']

#cursor = collections.find({})
#cursor = collections.find({"BaseVolume": {"$gt": 100000}})
cursor = collections.find({"MarketName": "BTC-NEO"}).sort("TimeStamp", -1)

printLastNumber(cursor , 5)

#for document in cursor: 
#    pprint(document)
#    #print document.keys()
#    print '-----------------------------------------------------------------------------------------------------------------------------------------------'

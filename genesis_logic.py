#!/usr/bin/env python2.7

import json
import requests
from pprint import pprint
from pymongo import MongoClient
from time import sleep


client = MongoClient()

db = client['bittrex']

collections = db['marketSummaries']

cursor = collections.find({"BaseVolume": {"$gt": .1}})

for document in cursor: 
    pprint(document)
    print '-----------------------------------------------------------------------------------------------------------------------------------------------'

#!/usr/bin/env python2.7

import json
import requests
from pprint import pprint
from pymongo import MongoClient
from time import sleep


client = MongoClient(host=['192.168.1.198:27017'])

db = client['bittrex']

collections = db['marketSummaries']

cursor = collections.find({})

for document in cursor:
    pprint(document)
    print '-----------------------------------------------------------------------------------------------------------------------------------------------'

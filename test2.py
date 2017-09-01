import time
import requests
import numpy
import json
from collections import deque
from pprint import pprint

def getXValues(x_count, time_interval):
	x_list = []
	
	while x_count >= 0:
		x_list.append(x_count)
		x_count = (x_count - 1) * time_interval

	return x_list

time_interval = 5	
		
myNewList = list()

maxlen = 5

myList = deque('', maxlen)

counter = 0

while counter < maxlen:

	localtime = time.asctime( time.localtime(time.time()) )

	r = requests.get("https://bittrex.com/api/v1.1/public/getticker?market=BTC-NEO")

	data = r.json()
	res = data["result"]
	last = res["Last"]
	
	myList.append(last)
	
	myNewList = list(myList)
	
	counter = counter + 1
	
	print "Local current time :", localtime
	
	print(last)
	#print(myList)
	print(myNewList)
	
	time.sleep(time_interval)

while True:

	localtime = time.asctime( time.localtime(time.time()) )

	r = requests.get("https://bittrex.com/api/v1.1/public/getticker?market=BTC-NEO")

	data = r.json()
	res = data["result"]
	last = res["Last"]
	
	myList.append(last)
	
	myNewList = list(myList)
	
	y = numpy.array(myNewList)
	z = numpy.polyfit(getXValues(maxlen, time_interval), y, 3)
	f = numpy.poly1d(z)
	fprime = f.deriv(1)
	
	print "Local current time :", localtime
	
	print fprime(0)
	
	print(last)
	#print(myList)
	print(myNewList)
	print "NEW SHIT NEW SHIT NEW SHIT"
	
	time.sleep(time_interval)
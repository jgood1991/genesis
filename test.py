import time
import requests
import numpy
import json
from collections import deque
from pprint import pprint

myNewList = list()

myList = deque('', maxlen=5)

while True:

	localtime = time.asctime( time.localtime(time.time()) )

	r = requests.get("https://bittrex.com/api/v1.1/public/getticker?market=BTC-NEO")

	data = r.json()
	res = data["result"]
	last = res["Last"]
	
	myList.append(last)
	
	myNewList = list(myList)
	
	counter = 0
	
	if(counter > 4):
		x = numpy.array([20.0, 15.0, 10.0, 5.0, 0.0])
		y = numpy.array(myNewList)
		z = numpy.polyfit(x, y, 3)
	return(z)	
	
	counter = counter + 1
	
	print "Local current time :", localtime
	
	print(last)
	#print(myList)
	print(myNewList)
	
	time.sleep(1)
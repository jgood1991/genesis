import time
import requests
import numpy
import json
from collections import deque

list = deque('00000', maxlen=5)

while True:

	localtime = time.asctime( time.localtime(time.time()) )

	r = requests.get("https://bittrex.com/api/v1.1/public/getticker?market=BTC-NEO")

	data = r.json()
	res = data["result"]
	last = res["Last"]
	
	list.append(last)
	
	#x = numpy.array([20.0, 15.0, 10.0, 5.0, 0.0])
	#y = numpy.array(list)
	#z = numpy.polyfit(x, y, 3)
	
	print "Local current time :", localtime
	
	print(last)
	print (list)
	
	time.sleep(5)
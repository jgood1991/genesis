import time
import requests
import numpy
import json
from collections import deque
from pprint import pprint

time_period = 2	

myNewList = list()

max_len = 30

x_count = max_len

myList = deque('', maxlen = max_len)

counter = 0

x_list = []
	
while x_count > 0:
	x_count = x_count - 1
	x_list.append(x_count)
	
new_x_list = [i * time_period for i in x_list]

while counter < max_len:

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
	#print(myNewList)
	#print(new_x_list)
	
	time.sleep(time_period)
	
#defining states 0 is init state, 1 is bought and holding waiting for sell conditions, 2 is sold waiting for buy conditions
states = [0,1,2]
#the master state list 0 is market, 1 is the state, 2 is previous derivative, and 3 is current derivative
stateList = ["BTC-NEO", 0, 0 , 0]
posDerivThreshold = 0.0000002
negDerivThreshold = -0.0000001
lcounter = 0
myFile = open("orderbook.txt", "w")
bought_last = 0.0

while True:

	myFile = open("orderbook.txt", "a")

	localtime = time.asctime( time.localtime(time.time()) )

	r = requests.get("https://bittrex.com/api/v1.1/public/getticker?market=BTC-NEO")

	data = r.json()
	res = data["result"]
	last = res["Last"]
	
	myList.append(last)
	
	myNewList = list(myList)
	
	x = numpy.array(x_list)
	y = numpy.array(myNewList)
	z = numpy.polyfit(x, y, 3)
	f = numpy.poly1d(z)
	fprime = f.deriv(1)
	
	stateList[3] = fprime(0)
	if stateList[1] == 0 and stateList[3] > posDerivThreshold:
		print "BUYBUYBUYBUYBUYBUYBUYBUYBUY at the price of " + str(last)
		myFile.write("BUYBUYBUYBUYBUYBUYBUYBUYBUY at the price of " + str(last) + "\n"  )
		stateList[1] = 1
		bought_last = last
		myFile.close()

	#if stateList[1] == 1 and stateList[3] < negDerivThreshold:
	if stateList[1] == 1 and stateList[3] < negDerivThreshold and last - bought_last > .0025 * bought_last + .0025 * last:
		print "SELLSELLSELLSELLSELLSELLSELLSELL at the price of " + str(last)
		myFile.write("SELLSELLSELLSELLSELLSELLSELLSELL at the price of " + str(last) + "\n")
		stateList[1] = 2
		myFile.close()
	elif stateList[1] == 1 and last <= bought_last * 0.985:
		print "SELLSELLSELLSELLSELLSELLSELLSELL at the price of " + str(last)
		myFile.write("SELLSELLSELLSELLSELLSELLSELLSELL at the price of " + str(last) + "\n")
		stateList[1] = 2
		myFile.close()

	if stateList[1] == 2 and stateList[3] > posDerivThreshold:
		print "BUYBUYBUYBUYBUYBUYBUYBUYBUY at the price of " + str(last)
		myFile.write("BUYBUYBUYBUYBUYBUYBUYBUYBUY at the price of " + str(last) + "\n")
		stateList[1] = 1
		myFile.close()
	
	print "Local current time :", localtime
	
	print(last)
	print "bought_last = " + str(bought_last)
	
	print fprime(0)
	
	#print(myList)
	#print(myNewList)
	print "NEW SHIT NEW SHIT NEW SHIT"
	myFile.close()
	
	time.sleep(time_period)
	
myFile.close()
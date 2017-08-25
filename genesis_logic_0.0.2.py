#!/usr/bin/env python2.7
import matplotlib
matplotlib.use('Agg')
import json
import requests
import numpy
from datetime import datetime
from pprint import pprint
from pymongo import MongoClient
from time import sleep
import matplotlib.pyplot as plt


#Function that returns a list[last, time, market] of the last NUMBER of samples for MARKET where the first element in the list is the latest data point and the last element in the list is the oldest datapoint. All elements in list are unique
def printLastNumbers( market , number):
	myGraphList = []
	cursor = collections.find({"MarketName": market }).sort("TimeStamp", -1)
	for document in cursor:
		#pprint(document['Ask'])
		#pprint(document['TimeStamp'])
		#pprint(document['MarketName'])
		myGraphList.append([document['Last'],document['TimeStamp'],document['MarketName']])
		#mySetTemp = set(myGraphList)
		#myGraphList = [list(t) for t in set(tuple(element) for element in myGraphList)]
		#number = number - 1
		if (number == len(myGraphList)):
			myGraphList = sorted(myGraphList,key=lambda l:l[1], reverse=True)
			return myGraphList
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
		if responseList[counterI]["BaseVolume"] > 1000:
			myMarketList.append(responseList[counterI]['MarketName'])
		#print "______________________________________________________________________________________________________________________________________________________"
	return myMarketList


#Input printLastNumbers list and returns new list with timestamp converted datetime format
def parseTimeStamps(myList):
	for x in myList:
		format = '%Y-%m-%d %H:%M:%S'
		x[1] = str(x[1]).replace("T", " ")
		x[1] = str(x[1]).split(".", 1)[0]
		#print x[2] + "---------------" + x[1] + "-----------" + str(datetime.strptime(x[1], format))
		x[1] = datetime.strptime(x[1], format)

	return myList

#returns list of last price and time in seconds normalized to 0   where 0 is the lastest  time sample available
def normalizeTimeStamps(myList):
	normalizedList = []
	howLong = len(myList)
	counterI = 0
	while counterI < howLong  :
		#myList[counterI][1] = str(myList[0][1] - myList[counterI][1])
		#print myList[0][1] - myList[counterI][1]
		normalizedList.append([myList[counterI][0], (myList[0][1] - myList[counterI][1]).total_seconds(), myList[0][2]])
		counterI = counterI + 1

	return normalizedList

def getPolyFitCoords(xylist):
	for x in xylist:
		x[1] = x[1] * -1

	return xylist



#Returns a list of the latest Changes to a particular market for #of samples where each element is a list of col0 is %change adjcent col1 is time from previous sample col2 is %change from past col3 is time from past samples to now and col4 is the market
def getLatestChangeList(market, samples):
	myChangeList = []
	counter = 0
	masterList = normalizeTimeStamps(parseTimeStamps(printLastNumbers(market, samples)))
	while counter < samples - 1:
		myChangeList.append([ ((masterList[counter][0] - masterList[counter + 1][0]) /  masterList[counter][0] ) * 100,  (masterList[counter + 1][1] - masterList[counter ][1]),  ((masterList[0][0] - masterList[counter + 1][0]) /  masterList[0][0] ) * 100, (masterList[counter + 1][1]) , masterList[counter][2]])
		counter = counter + 1
	myChangeList = sorted(myChangeList,key=lambda l:l[3], reverse=False)
	return myChangeList


def calcMovingAverage(changeList):
	#print len(changeList)
	valuesList = []
	sumValues = 0
	counter = 1
	while counter < len(changeList)  :
		valuesList.append(changeList[counter][0])
		sumValues = changeList[counter][0] + sumValues
		counter = counter + 1
	averageValue = sumValues /  (len(changeList) -1)
	#print "Current value of " + str(changeList[0][4]) + " " + str(changeList[0][0]) + ", Average for previous values " + str(numpy.mean(valuesList)) + ", STDDEV for previous values " + str(numpy.std(valuesList))
	#print numpy.mean(valuesList)
	#print numpy.std(valuesList)
	if ((changeList[2][2] / 3) - numpy.mean(valuesList)) > (numpy.std(valuesList)) and changeList[0][0] > 0 :
	#if ((changeList[0][0] ) - numpy.mean(valuesList)) > (numpy.std(valuesList)) and changeList[0][0] > 0 :
		pprint(changeList)
		print "Current value of " + str(changeList[0][4]) + " " + str(changeList[0][0]) + ", Average for previous values " + str(numpy.mean(valuesList)) + ", STDDEV for previous values " + str(numpy.std(valuesList)) + " average of last 3 " + str((changeList[2][2] / 3))
		print "BUYBUYBUYBUYBUYBUYBUYBUYBUY"

def getCurrentDerivative(market, samples):
	mlist = getPolyFitCoords(normalizeTimeStamps(parseTimeStamps(printLastNumbers(market, samples))))
	#pprint(mlist)
	xcoords = []
	ycoords = []
	xycoords = []
	for y in mlist:
		xcoords.append(y[1])
		ycoords.append(y[0])
		xycoords.append([y[1],y[0]])

	#pprint(xcoords)
	#pprint(ycoords)
	x = numpy.array(xcoords)
	y = numpy.array(ycoords)
	z = numpy.polyfit(x, y,37 )
	#pprint(z)
	#print str(z[0]) + "x^3+" +  str(z[1]) + "x^2+" + str(z[2]) + "x^1+" + str(z[3])
	# + str(z[4]) + "x"
	# + str(z[5]) + "x^5+" + str(z[6]) + "x^4+" + str(z[7]) + "x^3+" + str(z[8]) + "x^2+" + str(z[9]) + "x+" + str(z[10])
	#plt.plot(xcoords,ycoords)
	#plt.show()
	#plt.savefig('plot.png')
	f = numpy.poly1d(z)
	#print f
	fprime = f.deriv(1)
	# calculate new x's and y's
	x_new = numpy.linspace(xcoords[0], xcoords[-1], 1000)
	y_new = f(x_new)

	plt.figure(0)
	plt.plot(xcoords,ycoords)
	plt.plot( x_new, y_new)
	#plt.plot(x,y,'o', x_new, y_new)
	plt.savefig('plot.png')

	y_new = fprime(x_new)
	plt.figure(1)
	plt.plot( x_new, y_new)
	plt.savefig('plotd.png')
	#print fprime(0)
	return [fprime(0),mlist[0]]


#Establishing connection to MongoDB database
client = MongoClient(host=['192.168.1.198:27017'])
#client = MongoClient(host=['108.196.157.14:27017'])

db = client['bittrex']

collections = db['marketSummaries']
# Connection Established


#printLastNumbers( "BTC-LSK" , 50)
#pprint(getMarkets())
#print getMarkets()
##########masterList = normalizeTimeStamps(parseTimeStamps(printLastNumbers("BTC-ARK", 600)))
#masterList = parseTimeStamps(printLastNumbers("BTC-INCNT", 250))
#############print str((  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] ) ) + "_______" + masterList[0][2]
#print (  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] )
#pprint(masterList)
#for x in masterList:
#	print str(x[0]) + "-----------" + str(x[1])
#print masterList[0][1] - masterList[3][1]

#mlist = getLatestChangeList("USDT-BTC", 23)
#pprint(mlist)
#calcMovingAverage(mlist)


# while True:
# 	for x in getMarkets():
# 		mlist = getLatestChangeList(x, 100)
# 	#pprint(mlist)
# 		calcMovingAverage(mlist)
# 	print ""








#matplotlib.use('Agg')
# mlist = getPolyFitCoords(normalizeTimeStamps(parseTimeStamps(printLastNumbers("BTC-BTA", 400))))
# pprint(mlist)
# xcoords = []
# ycoords = []
# xycoords = []
# for y in mlist:
# 	xcoords.append(y[1])
# 	ycoords.append(y[0])
# 	xycoords.append([y[1],y[0]])
#
# #pprint(xcoords)
# #pprint(ycoords)
# x = numpy.array(xcoords)
# y = numpy.array(ycoords)
# z = numpy.polyfit(x, y,50 )
# #pprint(z)
# #print str(z[0]) + "x^3+" +  str(z[1]) + "x^2+" + str(z[2]) + "x^1+" + str(z[3])
# # + str(z[4]) + "x"
# # + str(z[5]) + "x^5+" + str(z[6]) + "x^4+" + str(z[7]) + "x^3+" + str(z[8]) + "x^2+" + str(z[9]) + "x+" + str(z[10])
# #plt.plot(xcoords,ycoords)
# #plt.show()
# #plt.savefig('plot.png')
# f = numpy.poly1d(z)
# print f
# fprime = f.deriv(1)
# # calculate new x's and y's
# x_new = numpy.linspace(xcoords[0], xcoords[-1], 1000)
# y_new = f(x_new)
#
# plt.figure(0)
# plt.plot(xcoords,ycoords)
# plt.plot( x_new, y_new)
# #plt.plot(x,y,'o', x_new, y_new)
# plt.savefig('plot.png')
#
# y_new = fprime(x_new)
# plt.figure(1)
# plt.plot( x_new, y_new)
# plt.savefig('plotd.png')
# print fprime(0)

#defining states 0 is init state, 1 is bought and holding waiting for sell conditions, 2 is sold waiting for buy conditions
states = [0,1,2]
#the master state list 0 is market, 1 is the state, 2 is previous derivative, and 3 is current derivative
stateList = ["BTC_HKG", 0, 0 , 0]
posDerivThreshold = 0
negDerivThreshold = 0
lcounter = 0
while True:
	myderivList = getCurrentDerivative("BTC-HKG", 400)
	myderiv = myderivList[0]
	currentPriceForCoin = myderivList[1]
	stateList[2] = stateList[3]
	stateList[3] = myderiv
	if stateList[1] == 0 and stateList[2] <= 0 and stateList[3] > posDerivThreshold:
		print "BUYBUYBUYBUYBUYBUYBUYBUYBUY at the price of " + str(currentPriceForCoin)
		stateList[1] = 1

	if stateList[1] == 1 and stateList[2] >= 0 and stateList[3] < posDerivThreshold:
		print "SELLSELLSELLSELLSELLSELLSELLSELL at the price of " + str(currentPriceForCoin)
		stateList[1] = 2

	if stateList[1] == 2 and stateList[2] <= 0 and stateList[3] > posDerivThreshold:
		print "BUYBUYBUYBUYBUYBUYBUYBUYBUY at the price of " + str(currentPriceForCoin)
		stateList[1] = 1
	lcounter = lcounter + 1
	print lcounter




#pprint(printLastNumbers("BTC-OMG", 250))
###displayList = []
###loopList = range(500)
###loopList.pop(0)
###loopList.pop(0)
#loopList.pop(0)
#print loopList
#for x in getMarkets():
###lenOfSamples = 500
###counter = 0
###masterList = normalizeTimeStamps(parseTimeStamps(printLastNumbers("BTC-THC", lenOfSamples)))
	#pprint(masterList)
###while counter < lenOfSamples - 1:
###	displayList.append([ ((masterList[counter][0] - masterList[counter + 1][0]) /  masterList[counter][0] ) * 100,  (masterList[counter + 1][1] - masterList[counter ][1]),  ((masterList[0][0] - masterList[counter + 1][0]) /  masterList[0][0] ) * 100, masterList[counter + 1][1], masterList[counter][2]])
###	counter = counter + 1
	#print str((  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] ) ) + "_______" + masterList[0][2] + "______________" + str(masterList[len(masterList)-1][1])
	#displayList.append([(  masterList[0][0] - masterList[len(masterList)-1][0]  ) / (  masterList[len(masterList)-1][1] ), masterList[0][2], masterList[0][0] - masterList[len(masterList)-1][0] , masterList[len(masterList)-1][1] , ((masterList[0][0] - masterList[len(masterList)-1][0]) / masterList[0][0]) * 100  ] )
	#displayList.append([ masterList[0][2],  (masterList[len(masterList)-1][1])/60 , ((masterList[0][0] - masterList[len(masterList)-1][0]) / masterList[0][0]) * 100  ] )

#displayList = sorted(displayList,key=lambda l:l[4], reverse=True)
###displayList = sorted(displayList,key=lambda l:l[3], reverse=False)
###pprint(displayList)
	#pprint(printLastNumbers( x , 100))
	#print "______________________________________________________________________________________________________________________________________________________"
	#print "______________________________________________________________________________________________________________________________________________________"
	#print "______________________________________________________________________________________________________________________________________________________"

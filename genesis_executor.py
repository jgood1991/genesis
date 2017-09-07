#!/usr/bin/env python2.7

from bittrex import bittrex

import os

import subprocess



#Get these from https://bittrex.com/Account/ManageApiKey

api = bittrex('key', 'secret')



directory = "C:\Users\goodj"



def executor():

	#Market to buy/sell at from Anre's script

	trade = 'BTC'

	#currency will be replaced with BUY or SELL currency from Anre's script

	currency = 'NEO'

	market = '{0}-{1}'.format(trade, currency)

	#buySell = info from Anre's script



	#Getting the BTC balance

	BTCbalance = api.getbalance(trade)

	BTC = BTCbalance['Available']

	#print BTC

	print "Your balance is {0} {1}.".format(BTCbalance['Available'], trade)



	#Determining BTC to spend per transaction

	percentPerOrder = 0.2



	#Getting the BTC price for currency

	currencySummary = api.getmarketsummary(market)

	currencyPrice = currencySummary[0]['Last']

	print 'The price for {0} is {1:.8f} {2}.'.format(currency, currencyPrice, trade)



	#Buying amount of currency

	#if buySell = 'BUYBUYBUYBUY':

		#percentAbove = 0.01

		#buyPrice = currencyPrice + currencyPrice * percentAbove

		#amount = (BTC * percentPerOrder) / buyPrice

		#print amount

		#print buyPrice

		#print 'Buying {0} {1} for {2:.8f} {3}.'.format(amount, currency, buyPrice, trade)

		#api.buylimit(market, amount, buyPrice)



	#Selling currency

	#elif buySell = 'SELLSELLSELLSELL':

		#amount = api.getbalance(currency)

		#print 'Selling {0} {1} for {2:.8f} {3}.'.format(amount, currency, currencyPrice, trade)

		#api.sellmarket(market, amount)


uuidOrderList = [["USDT_BTC", "0d3c8316-4e30-432f-9c3d-99ee4a736a94"],["USDT_NEO", "0d3c8316-4e30-432f-9c3d-99ee4a736a95"]]
counterTester = 1
while True:

	for filename in os.listdir(directory):

		if filename.endswith(".txt"):

			#print filename

			with open(filename) as file:
				if os.stat(filename).st_size == 0:
					pass
				else:
					last_line = file.readlines()[-1]
					splitString = last_line.split()
					myMarket = splitString[3]
					myUUID = splitString[4]
					orderType = splitString[1]
					orderPrice = splitString[2]
					for x in uuidOrderList:
						print x
						if x[0] == myMarket and x[1] == myUUID:
							pass
						elif x[0] == myMarket:
							# DO ORDER
							#print "SMALL"
							x[1] = myUUID
						else:
							# DO ORDER
							#print "BIG"
							uuidOrderList.append([myMarket, myUUID])


					#print splitString


			#line = subprocess.check_output(['tail', '-1', filename])

			#print line

			continue

		else:

			continue

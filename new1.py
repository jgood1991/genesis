#!/usr/bin/env python
from bittrex import bittrex

#Get these from https://bittrex.com/Account/ManageApiKey
api = bittrex('8318903750734cf0bac21716f6f1737b', '69b6ee5686504811b92ff6ece266c83f')

while True:
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
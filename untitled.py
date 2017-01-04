from collections import namedtuple
import sys

""" Stores information of a fill operation

	time: timestamp of the fill message
	name: name of the stock
	price: price of the stock at the time of the operation
	size: fill size of the stock,
	mode: side indicator; 'B' or 'S'

"""
Trade = namedtuple('Trade',['time','price','quantity','side','bid','ask','liquidity'])
TradeMessage = namedtuple('TradeMessage',['time','symbol','side','price','quantity'])

""" Stores information of a price update
	
	time: timestamp of the price update message
	name: name of the stock
	price: new stock price
"""
Quote = namedtuple('PriceMessage', ['time','name','price'])

from collections import namedtuple
import sys

""" Stores information of a fill operation

	time: timestamp of the fill message
	name: name of the stock
	price: price of the stock at the time of the operation
	size: fill size of the stock,
	mode: side indicator; 'B' or 'S'

"""
FillMessage = namedtuple('FillMessage',['time','name','price','size','mode'])

""" Stores information of a price update
	
	time: timestamp of the price update message
	name: name of the stock
	price: new stock price
"""
PriceMessage = namedtuple('PriceMessage', ['time','name','price'])


class StockTracker:
	""" Keep the information of stock
		
		Attributes:
		time: timestamp
		name: name of the stock
		cash: cash associated with the stock at the time
		size: the size of the stock owned at the time

	"""

 	def __init__(self, fill):
		""" Initialize an instance of StockTracker from a FillMessage.
			Assume initially cash = 0, size = 0. For example, If the side 
			indicator of the message is 'B', size = stock.size
			cash = -1*stock.size*stock.size. With a 'S' indicator, the 
			cash is positive and size is negative.
		
			Argument:
			stock -- namedtuple FillMessage
		"""
		if not isinstance(fill, FillMessage):
			raise ValueError('Not a valid stock')
 		self.name = fill.name
 		self.cash = 0
 		self.size = 0
 		self.update_position(fill)
 
	
	def update_position(self,fill):
		"""Given a sell/buy information of a stock, update the time,cash,
			and size holding of the very stock

			Arguments: 
			stock -- a instance of namedtuple Stock
		"""
		if self.name != fill.name:
			raise ValueError("Unmatched stock name")
		self.time = fill.time
		if fill.mode == 'B':
			self.size += fill.size
			self.cash -= fill.price*fill.size
		elif fill.mode == 'S':
			self.size -= fill.size
			self.cash += fill.price*fill.size
		else:
			raise ValueError('Unknown operation of the stock')


class PNLTracker:
	""" Manages holding positions of tracked stocks and output stock P&L when 
		new stock prices are available
		
		Atttribute:
		equities: a dictionary with stock names as keys and StockTracker instances
		as values.	
	"""

	def __init__(self):
		self.equities = {}
	
	def update_holding(self,fill):
		""" Update the holding information for a fill message

			Given a fill information, update the position of the stock;
			if the stock is not registered, generate new StockTracker for the stock

		    Argument:
			stock -- namedtuple Stock
		"""

		if fill.name in self.equities:
			self.equities[fill.name].update_position(fill)
		else:
			self.equities[fill.name] = StockTracker(fill)		

	def output_pnl(self, price, out=sys.stdout):
		""" Output the pnl information given the current price
	
			Given a price information, print out the current P&L based on the 
			size of holding and the new price

			If the price.name is not in the dictionary equities, output 
			warning "Do not own the stock"
		
		    Argument:
			price -- namedtuple PriceMessage

		"""
		if price.name not in self.equities:
			print "Warning: do not own this stock"
		else:
			value = self.equities[price.name].size*price.price + self.equities[price.name].cash
			out_info = ['PNL', str(price.time), price.name, str(self.equities[price.name].size), str(value)]
			out.write(' '.join(out_info)+'\n')
		
	def receive_information(self, info, out=sys.stdout):
		""" Given a message (fill/price information), update the holding information 
			or output the current pnl		
			Argument:
			info -- namedtuple FillMessage/PriceMessage
		"""
		if type(info).__name__ == 'FillMessage':
			self.update_holding(info)
		elif type(info).__name__ == 'PriceMessage':
			self.output_pnl(info,out)
		else:
			raise ValueError('Unknown  information')
	
class MessageDispatcher:
	""" Extract data from text file and parse data into PriceMessage/FillMessage

		Read in data from "fills" and "prices" file. Transfrom the string 
		to namedtuple PriceMessage/FillMessage. Return a generator to dispatch messages.

		Attributes:
		fills: string, the path of the file "fills"
		prices: string, the path of teh file "prices"
	"""

	def __init__(self, fills, prices):
		""" Initialize an instance from files' path		

		"""
		self.fills = fills
		self.prices = prices		

	def info_flow_generator(self):
		""" Extract data from the two files. Parse the data and 
			generate information in a time order
			Return:
				A generator which generate a FillMessage or PriceMessage
		""" 

		with open(self.fills,'r') as file1:
			fills = file1.read().strip(' \n').split('\n')
		with open(self.prices,'r') as file2:
			prices = file2.read().strip(' \n').split('\n')
		i, j  = 0, 0

		while True:
			if i == len(fills) and j == len(prices):
				break 
			elif i == len(fills):
				yield self.string_to_struct(prices[j])
				j += 1
			elif j == len(prices):
				yield self.string_to_struct(fills[i])
				i += 1
			else:
		
				if fills[i].split()[1] < prices[j].split()[1]:
					yield self.string_to_struct(fills[i])
					i += 1
				else:
					yield self.string_to_struct(prices[j])
					j += 1 
	
	@staticmethod
	def string_to_struct(string):
		""" Given a string, parse the string into namedtuple Price/Stock form
			Return:	
				a namedtuple FillMessage/PriceMessage
		"""
		message_ = string.split()
		if len(message_) != 6 and len(message_) != 4:
			raise ValueError('Unknown type of message')
		

		if message_[0] == 'F':
			time, name, price, size, mode = message_[1:]
			try:
				price = float(price)
				size = int(size)
				message = FillMessage(time, name, price, size, mode)
			except ValueError:
				print "Unknown message"
				raise
		elif message_[0] == 'P':
			time, name, price = message_[1:]
			try:	
				price = float(price)
				message = PriceMessage(time, name, price)
			except ValueError:
				print "Unknown message"
				raise
		return message



		

		

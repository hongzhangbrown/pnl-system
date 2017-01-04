#!/usr/bin/env python
from pnl import *
from StringIO import StringIO
import unittest


class TestPNL(unittest.TestCase):


	def setUp(self):
		self.stock_tracker = StockTracker(FillMessage(0,'MSFT',100,10,'B'))
		self.pnl_tracker = PNLTracker()
		
	def test_sell(self):
		fill = FillMessage(1,'MSFT',200,20,'S')
		update = self.stock_tracker.update_position(fill)
		Test = (self.stock_tracker.size == -10) and (self.stock_tracker.cash == 3000)\
		and (self.stock_tracker.time == 1)   
		self.assertEqual(Test,True)

	def test_buy(self):
		fill = FillMessage(2,'MSFT',100,60,'B')
		update = self.stock_tracker.update_position(fill)
		Test = (self.stock_tracker.size == 70) and (self.stock_tracker.cash == -7000)\
		and (self.stock_tracker.time == 2)   
		self.assertEqual(Test,True)

	def test_invalid_name(self):
		fill = FillMessage(2,'APPL',100,60,'B')
		self.assertRaises(ValueError, self.stock_tracker.update_position, fill)

	def test_update_price(self):
		self.pnl_tracker.receive_information(FillMessage(0,'APPL',100,30,'B'))
		self.pnl_tracker.receive_information(FillMessage(1,'APPL',150,10,'S'))
		out = StringIO()
		self.pnl_tracker.receive_information(PriceMessage(2,'APPL',200),out)
		output = out.getvalue().strip()
		assert output == 'PNL 2 APPL 20 2500'
	 
if __name__ == "__main__":
	unittest.main()

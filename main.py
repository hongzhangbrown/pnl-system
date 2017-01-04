#!/usr/bin/env python
from pnl import *


file1 = 'fills'
file2 = 'prices'

pnltracker = PNLTracker()
info = MessageDispatcher(file1,file2)
for info in info.info_flow_generator():
	pnltracker.receive_information(info)





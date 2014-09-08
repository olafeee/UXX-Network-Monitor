#!/usr/bin/env python
# Network Monitor
# version 1.0
# devoleped in Python v3
# tested in UBUNTU 12.04			  
# made by Olaf Elzinga & Nick de Bruijn Van Melis En Mariekerke	& Bas Alphenaar

from database import Database

class networkmonitor():
	def __init__(self, db):
		self.db = db


def main():
	#open session
	db = Database()
	db.toggleconnect()
	#act
	NM = networkmonitor(db)
	#close session
	db.disconnect()	
	#count time of all funtions



if __name__ == "__main__":	main()
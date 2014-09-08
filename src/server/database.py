import pymysql, time

class Database():
	def __init__(self):
		self.connected = False

	def toggleconnect(self):
		if(self.connected):
			self.disconnect()
			print("closed")
		else:
			self.connect()
			print("connect")

	# start connection and cursor
	def connect(self):
		self.conn = pymysql.connect(host='127.0.0.1',port=3306 , user='pyPDS', passwd='henkjan', db='PDS')
		self.cur = self.conn.cursor()

	#close cursor and connection
	def disconnect(self):
		self.cur.close()
		self.conn.close()

	# one function for selecting things out of db
	# @ stmnt = sql statement
	# @ arg = when blabla is used in statement
	def getInfo(self, stmnt, arg = None):
		if arg == None:
			self.cur.execute(stmnt)
		else:
			self.cur.execute(stmnt, arg)

		return self.cur.fetchall()
		

		print("y is", y)#mag weg
		self.cur.execute(UpdateDomain_count, (x+y, dateLog))
		self.conn.commit()
		return True

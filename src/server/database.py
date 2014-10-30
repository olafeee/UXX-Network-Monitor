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
		self.conn = pymysql.connect(host='127.0.0.1',port=3306 , user='root', passwd='henkjan', db='unix')
		self.cur = self.conn.cursor()

	#close cursor and connection
	def disconnect(self):
		self.cur.close()
		self.conn.close()

	def insertPacket(self, Dest_mac, Source_mac, eth_protocol):
		InsertStmt = "INSERT INTO ETH(Dest_mac,Source_mac,Protocol) VALUES (%s, %s, %s)"
		try:
			self.cur.execute(UpdateStmt, (Dest_mac, Source_mac, eth_protocol))
			self.conn.commit()
			result = True
		except:
			result = False

		return result

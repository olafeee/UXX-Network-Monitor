#Packet sniffer in python
#For Linux
 
import socket
 
#create an INET, raw socket
s = socket.socket()
host = socket.gethostname()
port = 12345
s.bind((host, port))

s.listen(5)
while True:
	c, addr = s.accept()
	print '########################################'
	print '#                                      #'
	print '#     Welcome to the Unix sniffer      #'
	print '#                                      #'
	print '########################################\n'
	print '#Got connection from', addr,' \n'
	c.send('#You are succesfully connected')
	c.close()

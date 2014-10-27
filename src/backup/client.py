#Packet sniffer in python
#For Linux
 
import socket, sys
from struct import *
 
#create an INET, raw socket
s = socket.socket()
host = socket.gethostname()
port = 12345

s.connect((host, port))
s.settimeout(1000)

while True:
	data  = s.recv(1024)
	if not data: 
		print "geen data"
		break
	print data

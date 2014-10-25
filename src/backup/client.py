#Packet sniffer in python
#For Linux
 
import socket, sys
from struct import *
 
#create an INET, raw socket
s = socket.socket()
host = socket.gethostname()
port = 12345

s.connect((host, port))

print s.recv(1024)

###########################Connection to server###########################

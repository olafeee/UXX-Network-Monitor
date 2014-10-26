#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
from struct import *
import sys
import time

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port

s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr

    try:
        sniff = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
    except socket.error , msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()     
    # receive a packet
    while True:
        pakket = ''
        packet = sniff.recvfrom(65565)
             
            #packet string from tuple
        packet = packet[0]
             
            #take first 20 characters for the ip header
        ip_header = packet[0:20]
             
            #now unpack them :)
        iph = unpack('!BBHHHBBH4s4s' , ip_header)
            
        version_ihl = iph[0]
        version = version_ihl >> 4
        ihl = version_ihl & 0xF
             
        iph_length = ihl * 4
            
        ttl = iph[5]
        protocol = iph[6]
        s_addr = socket.inet_ntoa(iph[8]);
        d_addr = socket.inet_ntoa(iph[9]);
             
        pakket = 'Version : ' + str(version) + ' IP Header Length : ' + str(ihl) + ' TTL : ' + str(ttl) + ' Protocol : ' + str(protocol) + ' Source Address : ' + str(s_addr) + ' Destination Address : ' + str(d_addr)
             
        tcp_header = packet[iph_length:iph_length+20]
             
            #now unpack them :)
        tcph = unpack('!HHLLBBHHH' , tcp_header)
           
        source_port = tcph[0]
        dest_port = tcph[1]
        sequence = tcph[2]
        acknowledgement = tcph[3]
        doff_reserved = tcph[4]
        tcph_length = doff_reserved >> 4
             
        pakket += 'Source Port : ' + str(source_port) + ' Dest Port : ' + str(dest_port) + ' Sequence Number : ' + str(sequence) + ' Acknowledgement : ' + str(acknowledgement) + ' TCP header length : ' + str(tcph_length)
             
        h_size = iph_length + tcph_length * 4
        data_size = len(packet) - h_size
             
            #get data from the packet
        data = packet[h_size:]
        

        c.send(pakket)
        c.close
        
         
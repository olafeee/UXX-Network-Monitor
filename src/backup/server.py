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
c, addr = s.accept()     # Establish connection with client.
i = 1
while True:
    print 'Got connection from', addr

    #Convert a string of 6 characters of ethernet address into a dash separated hex string
    def eth_addr (a) :
        b = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(a[0]) , ord(a[1]) , ord(a[2]), ord(a[3]), ord(a[4]) , ord(a[5]))
        return b

    #create a AF_PACKET type raw socket (thats basically packet level)
    #define ETH_P_ALL    0x0003          /* Every packet (be careful!!!) */
    try:
        tcp = socket.socket( socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
    except socket.error , msg:
        print 'Socket could not be created. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()

    #Recive a packet
    while True:
        packet = tcp.recvfrom(65565)
 
        #packet string from tuple
        packet = packet[0]

        #parse ethernet header
        eth_length = 14
 
        eth_header = packet[:eth_length]
        eth = unpack('!6s6sH' , eth_header)
        eth_protocol = socket.ntohs(eth[2])
        pakket = ' DMAC:' + eth_addr(packet[0:6]) + ' SMAC:' + eth_addr(packet[6:12]) + ' P:' + str(eth_protocol)
        #print 'Destination MAC.....: ' + eth_addr(packet[0:6]) + '\nSource MAC..........: ' + eth_addr(packet[6:12]) + '\nProtocol............: ' + str(eth_protocol)

        #Parse IP packets, IP Protocol number = 8
        if eth_protocol == 8 :
            #Parse IP header
            #take first 20 characters for the ip header
            ip_header = packet[eth_length:20+eth_length]
     
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

            pakket += 'V: ' + str(version) + 'IPHL: ' + str(ihl) + 'TTL: ' + str(ttl) + 'P: ' + str(protocol) + 'Sadd: ' + str(s_addr) + 'Dadd: ' + str(d_addr)
            print 

            #TCP protocol
            if protocol == 6 :
                t = iph_length + eth_length
                tcp_header = packet[t:t+20]

                #now unpack them :)
                tcph = unpack('!HHLLBBHHH' , tcp_header)
          
                source_port = tcph[0]
                dest_port = tcph[1]
                sequence = tcph[2]
                acknowledgement = tcph[3]
                doff_reserved = tcph[4]
                tcph_length = doff_reserved >> 4
                pakket += 'SPort:' + str(source_port) + 'DPort:' + str(dest_port) + 'Seq: ' + str(sequence) + 'Ack: ' + str(acknowledgement) + 'TCPhead: ' + str(tcph_length)
                #print 'Source Port.........: ' + str(source_port) + '\nDest Port...........: ' + str(dest_port) + '\nSequence Number.....: ' + str(sequence) + '\nAcknowledgement.....: ' + str(acknowledgement) + '\nTCP header length...: ' + str(tcph_length)
         
                h_size = eth_length + iph_length + tcph_length * 4
                data_size = len(packet) - h_size
         
                #get data from the packet
                data = packet[h_size:]
         
                #print 'Data : ' + data

            #ICMP Packets
            elif protocol == 1 :
                u = iph_length + eth_length
                icmph_length = 4
                icmp_header = packet[u:u+4]

                #now unpack them :)
                icmph = unpack('!BBH' , icmp_header)
         
                icmp_type = icmph[0]
                code = icmph[1]
                checksum = icmph[2]
                
                pakket += 'Type : ' + str(icmp_type) + ' Code : ' + str(code) + ' Checksum : ' + str(checksum)
         
                h_size = eth_length + iph_length + icmph_length
                data_size = len(packet) - h_size
         
                #get data from the packet
                data = packet[h_size:]
         
                #print 'Data : ' + data

            #UDP packets
            elif protocol == 17 :
                u = iph_length + eth_length
                udph_length = 8
                udp_header = packet[u:u+8]

                #now unpack them :)
                udph = unpack('!HHHH' , udp_header)
           
                source_port = udph[0]
                dest_port = udph[1]
                length = udph[2]
                checksum = udph[3]
                
                pakket += 'SPort:' + str(source_port) + ' DPort:' + str(dest_port) + ' Len:' + str(length) + ' Chk: ' + str(checksum)
                #print 'Source Port.........: ' + str(source_port) + '\nDest Port...........: ' + str(dest_port) + '\nLength..............: ' + str(length) + '\nChecksum............: ' + str(checksum)
         
                h_size = eth_length + iph_length + udph_length
                data_size = len(packet) - h_size
         
                #get data from the packet
                #data = packet[h_size:]
         
                #print 'Data : ' + data

            #some other IP packet like IGMP
            else :
                print 'Protocol other than TCP/UDP/ICMP'
         
            #print '_______________________________________'

            # om loops tegen te gaan
            # nu dport volgens mij straks sport
            if tcph[0] != port and tcph[1] != port:
                c.send(str(tcph[0]))
                i+=1
        
        #print "1"
        #c.close

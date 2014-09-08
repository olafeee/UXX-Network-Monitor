#!/usr/bin/env python2

import pcap
import sys
import string
import time
import socket
import struct
import pymysql, time

class sniff():
    def __init__(self):
       protocols={socket.IPPROTO_TCP:'tcp',
           socket.IPPROTO_UDP:'udp',
           socket.IPPROTO_ICMP:'icmp'}

    connected = False

    def decode_ip_packet(self, s):
      d={}
      d['version']=(ord(s[0]) & 0xf0) >> 4
      d['header_len']=ord(s[0]) & 0x0f
      d['tos']=ord(s[1])
      d['total_len']=socket.ntohs(struct.unpack('H',s[2:4])[0])
      d['id']=socket.ntohs(struct.unpack('H',s[4:6])[0])
      d['flags']=(ord(s[6]) & 0xe0) >> 5
      d['fragment_offset']=socket.ntohs(struct.unpack('H',s[6:8])[0] & 0x1f)
      d['ttl']=ord(s[8])
      d['protocol']=ord(s[9])
      d['checksum']=socket.ntohs(struct.unpack('H',s[10:12])[0])
      d['source_address']=pcap.ntoa(struct.unpack('i',s[12:16])[0])
      d['destination_address']=pcap.ntoa(struct.unpack('i',s[16:20])[0])
      if d['header_len']>5:
        d['options']=s[20:4*(d['header_len']-5)]
      else:
        d['options']=None
      d['data']=s[4*d['header_len']:]
      d['src_port'] = int(socket.ntohs(struct.unpack('H',d['data'][0:2])[0]))
      d['dst_port'] = int(socket.ntohs(struct.unpack('H',d['data'][2:4])[0]))
      return d



    

    def print_packet(self, pktlen, data, timestamp):
      if not data:
        return

      if data[12:14]=='\x08\x00':
        decoded= self.decode_ip_packet(data[14:])
        if decoded['src_port']:
            src_port = decoded['src_port']
        if decoded['dst_port']:
            dst_port = decoded['dst_port']

        InsertStmt = "INSERT INTO Netmon_packets (version, protocol, id, header_len, tos, total_len, ttl, source_address, destination_address, src_port, dst_port) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.cur.execute(InsertStmt, (int(decoded['version']),
                                 str(decoded['protocol']),
                                 str(decoded['id']),
                                 str(decoded['header_len']),
                                 str(decoded['tos']),
                                 str(decoded['total_len']),
                                 int(decoded['ttl']),
                                 str(decoded['source_address']),
                                 str(decoded['destination_address']),
                                 int(decoded['src_port']),
                                 int(decoded['dst_port']),
            ))
        self.conn.commit()


        '''print '\n%s.%f %s > %s %s %s %s %s %s' % (time.strftime('%H:%M',
                                               time.localtime(timestamp)),
                                 timestamp % 60,
                                 decoded['source_address'],
                                 decoded['destination_address'],
                                 decoded['version'],
                                 decoded['dst_port'],
                                 decoded['tos'],
                                 decoded['tos'],
                                 decoded['tos'],
                                 )'''
 
    def toggleconnect(self):
        if(self.connected):
            self.disconnect()
            print "closed"
        else:
            self.connect()
            print "connect"

    # start connection and cursor
    def connect(self):
        self.conn = pymysql.connect(host='127.0.0.1',port=3306 , user='pyPDS', passwd='henkjan', db='netmon')
        self.cur = self.conn.cursor()

    #close cursor and connection
    def disconnect(self):
        self.cur.close()
        self.conn.close()
        


def main():
    sc = sniff()
    sc.toggleconnect()

    if len(sys.argv) < 3:
        print ('usage: sniff.py <interface> <expr>')
        sys.exit(0)
    p = pcap.pcapObject()
    dev = sys.argv[1]
    net, mask = pcap.lookupnet(dev)
    # note:    to_ms does nothing on linux
    p.open_live(dev, 1600, 0, 100)
    #p.dump_open('dumpfile')
    p.setfilter(string.join(sys.argv[2:],' '), 0, 0)

    # try-except block to catch keyboard interrupt.    Failure to shut
    # down cleanly can result in the interface not being taken out of promisc.
    # mode
    #p.setnonblock(1)
    try:
        while 1:
            p.dispatch(1, sc.print_packet)

    except KeyboardInterrupt:
        sc.toggleconnect()
        print ('%s' % sys.exc_type)
        print ('shutting down')
        print ('%d packets received, %d packets dropped, %d packets dropped by interface' % p.stats())


    '''#open session
    db = Database()
    db.toggleconnect()
    #act
    pds = Pds(db)
    #pds.passiveDNS_logHandler(storeDB)
    pds.deleteData(dateLog)
    #close session
    db.disconnect() 
    #count time of all funtions
    latestTime=time.time() - t0
    print("time to run",latestTime)'''



if __name__ == "__main__":  main()
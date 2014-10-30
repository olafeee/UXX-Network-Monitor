#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import threading
import SocketServer
from struct import *

import curses
import time
import random
import sys
import linecache

pakketArray = []
kill_received = True
gpc = 0
packetsCount = 0
sock_error = 0
''''''
################################################
#                Start Server                  #
################################################

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

  def handle(self):
    global kill_received
    global gpc
    gpc = 10
    while True:
      if not kill_received:
        global pakketArray
        global packetsCount
        
        nump = len(pakketArray)
        del pakketArray[:]
        #num_client = threading.activeCount() - 1
        
        packetsCount +=nump
        fileWin(nump)
        
        cur_thread = threading.current_thread()
        response = "{}: {}".format(cur_thread.name, nump)
        try:
          self.request.sendall(response)
        except socket.error, e:
          global sock_error
          sock_error+=1

        time.sleep(1)
      elif kill_received:
        server.shutdown()
        time.sleep(10)
        print "exit"
        break

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass



def stopServer():
  kill_received = True

def stoppings(server):
  global kill_received
  global pakketArray
  while not kill_received:
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
        pakketArray.append(pakket)
    
    


################################################
#                Start Curses                  #
################################################
def init_curses():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    stdscr.bkgd(curses.color_pair(1))
    stdscr.refresh()
    return stdscr
 
def show_menu(win):
    win.clear()
    win.bkgd(curses.color_pair(2))
    win.box()
    win.addstr(1, 2, "i:", curses.A_UNDERLINE)
    win.addstr(1, 6, "messages")
    win.addstr(1, 20, "o:", curses.A_UNDERLINE)
    win.addstr(1, 24, "syslog")
    win.addstr(1, 38, "x:", curses.A_UNDERLINE)
    win.addstr(1, 42, "Exit")
    win.refresh()
    showFooter("win")


def read_file(menu_win, file_win, st):
    showFooter(st)
    menu_win.clear()
    menu_win.box()
    menu_win.addstr(1, 2, "x:", curses.A_UNDERLINE)
    menu_win.addstr(1, 5, "Ende ->")
    menu_win.refresh()
    file_win.box()
    file_win.clear()
    file_win.box()
    file_win.refresh()

    global kill_received
    while True:

      c = stdscr.getch()
      if c == ord('x'):
          kill_received = True
          break
    
    '''
    while True:

      c = stdscr.getch()
      if c == ord('x'):
          kill_received = True
          break

'''
def fileWin(packets):
  global file_win
  global packetsCount
  global sock_error
  file_win.clear()
  file_win.box()
  file_win.addstr(1, 2, "server is started")
  file_win.addstr(2, 2, "Packets send", curses.A_UNDERLINE)
  file_win.addstr(2, 22, str(packetsCount), curses.A_UNDERLINE)
  file_win.addstr(3, 2, "Connections closed", curses.A_UNDERLINE)
  file_win.addstr(3, 22, str(sock_error), curses.A_UNDERLINE)
  file_win.addstr(3, 2, "Connections openend", curses.A_UNDERLINE)
  file_win.addstr(3, 22, str(sock_error), curses.A_UNDERLINE)
  file_win.refresh()

def showFooter(st):
    global gpc
    histo_win = curses.newwin(4, 100, 26, 0)
    histo_win.box()
    histo_win.clear()
    histo_win.box()
    histo_win.addstr(1, 2, "Packetsniffer v0.3.1.3.6.8", curses.A_UNDERLINE)
    histo_win.addstr(1, 30, str(st) , curses.A_UNDERLINE)
    histo_win.addstr(1, 33, str(gpc) , curses.A_UNDERLINE)
    histo_win.refresh() 

if __name__ == "__main__":

  stdscr = init_curses()

  mwin = curses.newwin(3, 100, 0, 0)
  file_win = curses.newwin(22, 76, 4, 0)

  # Port 0 means to select an arbitrary unused port
  HOST, PORT = "localhost", 12753

  while True:
    stdscr.clear()
    stdscr.refresh()
    show_menu(mwin)
    showFooter("s")
    c = stdscr.getch()
    if c == ord('x'):
      break
    elif c == ord('i'):
      read_file(mwin, file_win, "i")
      show_menu(mwin)
      #showFooter("i")
    elif c == ord('o'):
      show_menu(mwin)
      kill_received = False
      #showFooter("o")

      # Port 0 means to select an arbitrary unused port
      HOST, PORT = "localhost", 12753

      server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
      ip, port = server.server_address

      # Start a thread with the server -- that thread will then start one
      # more thread for each request
      server_thread = threading.Thread(target=server.serve_forever)
      t4 = threading.Thread(target=stoppings, args=(server,))

      # Exit the server thread when the main thread terminates
      server_thread.daemon = True
      t4.daemon = True

      #Start Threads
      server_thread.start()
      t4.start()
      read_file(mwin, file_win, "ot")

  curses.nocbreak()
  stdscr.keypad(0)
  curses.echo()
  curses.endwin()

  print gpc

'''
stdscr = init_curses()

mwin = curses.newwin(3, 100, 0, 0)
file_win = curses.newwin(22, 80, 4, 0)

while True:
  stdscr.clear()
  stdscr.refresh()
  show_menu(mwin)
  showFooter("s")
  c = stdscr.getch()
  if c == ord('x'):
    break
  elif c == ord('i'):
    read_file(mwin, file_win, "i")
    show_menu(mwin)
    #showFooter("i")
  elif c == ord('o'):
    show_menu(mwin)
    kill_received = False
    #showFooter("o")
    try:
      t1 = Thread(target=runOften, args=("Ofthen Runs", file_win))
      t2 = Thread(target=runLessOften, args=("runLessOften Runs", file_win))
      t1.start()
      t2.start()

      read_file(mwin, file_win, "o")
    except Exception, e:
      print str(e)
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

print gpc
  



    #while not kill_received:
    #  client(ip, port, "Hello World 1")
    #  client(ip, port, "client 2")
    #  time.sleep(1)

'''

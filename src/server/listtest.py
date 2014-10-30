#!/usr/bin/python
# -*- coding: utf-8 -*-
import curses
import time
import random
import sys
import linecache
from threading import Thread

pakketArray = []
packetsCount = 0
kill_received = True

#collect the packets
def runOften(threadName, sleepTime):
  global kill_received
  while not kill_received:
    time.sleep(1)
    fileWin(4)
    global pakketArray
    pakketArray.append(random.random)


# send packets to the client
def runLessOften(threadName, sleepTime):
  global kill_received
  while not kill_received:
    time.sleep(1)
    global pakketArray
    global packetsCount
    packetsCount +=1
    fileWin(3)
    #print pakketArray
    del pakketArray[:]
    #print " \n hoi" + str(i) + "\n" + str(t1.isAlive())

 
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
    win.addstr(1, 2, "s:", curses.A_UNDERLINE)
    win.addstr(1, 6, "Start server")
    win.addstr(1, 20, "i:", curses.A_UNDERLINE)
    win.addstr(1, 24, "Exit")
    win.addstr(1, 38, "x:", curses.A_UNDERLINE)
    win.addstr(1, 42, "Exit")
    win.refresh()


def startServer(menu_win):
    filename = '/Users/olaffee/Pro/py/test.log'
    menu_win.clear()
    menu_win.box()
    menu_win.addstr(1, 2, "x:", curses.A_UNDERLINE)
    menu_win.addstr(1, 5, "Stop server ->")
    #menu_win.addstr(1, 14, filename)
    menu_win.refresh()
    
    '''
    file_win = curses.newwin(22, 80, 4, 0)
    file_win.box()
    line_start = 1
    line_max = 20
    ''
    while True:
      file_win.clear()
      file_win.box()
      for i in xrange(line_start, line_max + line_start):
          line = linecache.getline(filename, i)
          s = ''
          if len(line) > 60:
              s = '[%d %s]' % (i, line[:60])
          else:
              s = '[%d %s]' % (i, line[:-1])
          file_win.addstr(i - line_start + 1, 2, s)
      file_win.refresh()
      c = stdscr.getch()
      if c == ord('x'):
          break
      elif c == curses.KEY_UP:
          if line_start > 1:
              line_start -= 1
      elif c == curses.KEY_DOWN:
          line_start += 1

    '''
    fileWin(0)

    c = stdscr.getch()
    while True:
      if c == ord('x'):
          break
    
    '''old
    elif c == curses.KEY_UP:
        if line_start > 1:
            line_start -= 1
    elif c == curses.KEY_DOWN:
        line_start += 1'''

    
def fileWin(packets):
  global file_win
  global packetsCount
  file_win.clear()
  file_win.box()
  file_win.addstr(1, 2, "server is started")
  file_win.addstr(2, 2, "Packetsniffer v0.3.1.3.6.8", curses.A_UNDERLINE)
  file_win.addstr(3, 2, str(packets), curses.A_UNDERLINE)
  file_win.addstr(4, 2, str(packetsCount), curses.A_UNDERLINE)
  file_win.refresh()

def showFooter():
    histo_win = curses.newwin(4, 100, 26, 0)
    histo_win.box()
    histo_win.clear()
    histo_win.box()
    histo_win.addstr(1, 2, "Packetsniffer v0.3.1.3.6.8", curses.A_UNDERLINE)
    histo_win.addstr(1, 30, str(kill_received) , curses.A_UNDERLINE)
    histo_win.refresh() 

stdscr = init_curses()

mwin = curses.newwin(3, 100, 0, 0)
file_win = curses.newwin(22, 80, 4, 0)

while True:
  stdscr.clear()
  stdscr.refresh()
  show_menu(mwin)
  showFooter()
  c = stdscr.getch()
  if c == ord('x'):
    kill_received = True
    break
  elif c == ord('i'):
    startServer(mwin)
    show_menu(mwin)
  elif c == ord('s'):
    show_menu(mwin)
    kill_received = False
    try:
      startServer(mwin)
      t1 = Thread(target=runOften, args=("Ofthen Runs", 2))
      t2 = Thread(target=runLessOften, args=("runLessOften Runs", 2))
      t1.start()
      t2.start()
    except Exception, e:
      print str(e)
 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

'''

#!/usr/bin/python
# -*- coding: utf-8 -*-
import curses
import time
import random
import linecache
from threading import Thread

pakketArray = []
statusSniffer = False

def runOften(threadName, sleepTime):
  while True:
    time.sleep(1)
    pakketArray.append(random.random)

def runLessOften(threadName, sleepTime):
  while True:
    time.sleep(4)
    print pakketArray
    del pakketArray[:]
    print " \n hoi \n"

def runRandomly(threadName, sleepTime):
  while 1 < 2:
    time.sleep(sleepTime)
    print "%s" % (threadName)
 
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

def showFooter():
    histo_win = curses.newwin(4, 100, 26, 0)
    histo_win.box()
    histo_win.clear()
    histo_win.box()
    histo_win.addstr(1, 2, "Packetsniffer v0.3.1.3.6.8", curses.A_UNDERLINE)
    histo_win.addstr(1, 30, str(statusSniffer) , curses.A_UNDERLINE)
    histo_win.refresh() 

def read_file(menu_win, filename):
    menu_win.clear()
    menu_win.box()
    menu_win.addstr(1, 2, "x:", curses.A_UNDERLINE)
    menu_win.addstr(1, 5, "Ende ->")
    menu_win.addstr(1, 14, filename)
    menu_win.refresh()
    file_win = curses.newwin(22, 80, 4, 0)
    file_win.box()
    line_start = 1
    line_max = 20



    while True:
      file_win.clear()
      file_win.box()
      for i in xrange(line_start, line_max + line_start):
          line = linecache.getline(filename, i)
          s = ''
          if len(line) > 60:
              s = '[%d %s]' % (i, line[:60])
          else:
              s = '[%d %s]' % (i, line[:-1])
          file_win.addstr(i - line_start + 1, 2, s)
      file_win.refresh()
      c = stdscr.getch()
      if c == ord('x'):
          break
      elif c == curses.KEY_UP:
          if line_start > 1:
              line_start -= 1
      elif c == curses.KEY_DOWN:
          line_start += 1
 
stdscr = init_curses()

mwin = curses.newwin(3, 100, 0, 0)
 
while True:
  stdscr.clear()
  stdscr.refresh()
  show_menu(mwin)
  showFooter()
  c = stdscr.getch()
  if c == ord('x'):
    if statusSniffer:
      sys.exit()
      statusSniffer = False
      showFooter()
      break
x
  elif c == ord('i'):
    show_menu(mwin)
    statusSniffer = True
    showFooter()
    try:
      t1 = Thread(target=runOften, args=("Ofthen Runs", 2))
      t2 = Thread(target=runLessOften, args=("runLessOften Runs", 2))
      t1.start()
      t2.start()

      read_file(mwin, '/Users/olaffee/Pro/py/test.log')
    except Exception, e:
      print str(e)
 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

'''
'''

import time
import random
from threading import Thread

pakketArray = []
kill_received = False

def runOften(threadName, sleepTime):
	i = 0
	global kill_received
	while not kill_received:
		time.sleep(0.5)
		i+=1
		pakketArray.append(random.random)
		if i > 3:
			killAll()

def runLessOften(threadName, sleepTime):
	i = 0
	global kill_received
	while not kill_received:
		time.sleep(1)
		i+=1
		if i > 3:
			killAll()

		print pakketArray
		del pakketArray[:]
		print " \n hoi" + str(i) + "\n" + str(t1.isAlive())

def runRandomly(threadName, sleepTime):
	while 1 < 2:
		time.sleep(sleepTime)
		print "%s" % (threadName)

def killAll():
	global kill_received
	kill_received = True

t1 = Thread(target=runOften, args=("Ofthen Runs", 2))
t2 = Thread(target=runLessOften, args=("runLessOften Runs", 2))

def Main():
	try:
		t1.start()
		t2.start()
    
		print "Main complete"
	except Exception, e:
		print str(e)

if __name__ == '__main__':
	Main()
'''
'''

try:
	thread.start_new_thread(runOften, ("Ofthen Runs", 2))
	thread.start_new_thread(runLessOften, ("runLessOften Runs", 2))
	thread.start_new_thread(runRandomly, ("runRandomly Runs", random.random()))
except Exception, e:
	print str(e)
	'''
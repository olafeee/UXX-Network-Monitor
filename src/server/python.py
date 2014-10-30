#!/usr/bin/python
# -*- coding: utf-8 -*-
import curses
import time
import random
import sys
import linecache
from threading import Thread

pakketArray = []
kill_received = True
gpc = 0

def runOften(threadName, file_win):
  global kill_received
  while not kill_received:
    time.sleep(0.5)
    global pakketArray
    pakketArray.append(random.random)

def runLessOften(threadName, file_win):
  global kill_received
  while not kill_received:
    time.sleep(1)
    global pakketArray
    global gpc
    gpc += len(pakketArray)
    global gpc

    file_win.addstr(4, 20, str(gpc))
    file_win.refresh()
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
    file_win.addstr(4, 3, "P send")
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
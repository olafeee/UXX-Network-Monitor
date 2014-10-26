#!/usr/bin/python
# -*- coding: utf-8 -*-
import curses
import linecache
 
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
    win.addstr(1, 2, "F1:", curses.A_UNDERLINE)
    win.addstr(1, 6, "messages")
    win.addstr(1, 20, "F2:", curses.A_UNDERLINE)
    win.addstr(1, 24, "syslog")
    win.addstr(1, 38, "x:", curses.A_UNDERLINE)
    win.addstr(1, 42, "Exit")
    win.refresh()
 

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

    histo_win = curses.newwin(4, 100, 26, 0)
    histo_win.box()
    histo_win.clear()
    histo_win.box()
    histo_win.addstr(1, 2, "Packetsniffer v0.3.1.3.6.8", curses.A_UNDERLINE)
    histo_win.refresh()

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
  c = stdscr.getch()
  if c == ord('x'):
    break
  elif c == curses.KEY_F1:
    read_file(mwin, '/var/log/messages')
    show_menu(mwin)
  elif c == curses.KEY_F2:
    read_file(mwin, '/Users/olaffee/Pro/py/test.log')
    show_menu(mwin)
 
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()
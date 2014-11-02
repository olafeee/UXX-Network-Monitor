import socket
import threading
import SocketServer
import time, sys
import curses

kill_received = False

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

def showMenu(menuwin):
  menuwin.box()
  menuwin.bkgd(curses.color_pair(2))
  menuwin.addstr(1, 2, "X:", curses.A_UNDERLINE)
  menuwin.addstr(1, 6, "Exit")
  menuwin.refresh()

def showFooter(footerwin):
  footerwin.box()
  footerwin.addstr(1, 2, "Pakketsnuiver client", curses.A_UNDERLINE)
  footerwin.refresh()

def showLogWin(logwin):
  logwin.bkgd(curses.color_pair(2))
  logwin.box()
  # logwin.addstr(3, 3, "HEY", curses.A_UNDERLINE)
  logwin.refresh()

def logWinNewLine(newLine, logwin):
  logwin.clear()
  logwin.box()
  logwin.addstr(4, 4, newLine, curses.A_UNDERLINE)
  logwin.box()
  logwin.clear()
  logwin.refresh()

def client():
  ip = "127.0.0.1"
  port = 12753
  global kill_received
  global logwin
  # print "client start"
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ip, port))

  stdscr = init_curses()
  stdscr.immedok(True)

  menuwin = curses.newwin(3, 100, 0, 0)
  logwin = curses.newwin(22, 76, 4, 0)
  footer = curses.newwin(4, 100, 26, 0)

  stdscr.clear()
  stdscr.refresh()

  # while True:
  #   if not kill_received:
  #     print "hoi"

  #     # response = sock.recv(1024)
  #     # print "{}".format(response)

  #     # c = stdscr.getch()

  #     # if c == ord('s'):
  #     #   showMenu(menuwin)

  #     # logWinRefresh("TEST")

  #   else:
  #     sock.close()
  #     break

  while True:
    showMenu(menuwin)
    showFooter(footer)
    showLogWin(logwin)
    response = sock.recv(1024)
    logWinNewLine("hoi", logwin)
    # logwin.addstr(6, 4, "HEY", curses.A_UNDERLINE)
    stdscr.clear()
    stdscr.refresh()


  curses.nocbreak()
  stdscr.keypad(0)
  curses.echo()
  curses.endwin()

if __name__ == "__main__":

  client()
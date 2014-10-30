import socket
import threading
import SocketServer
import time, sys

kill_received = False

def client():
  ip = "127.0.0.1"
  port = 12753
  global kill_received
  print "client start"
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.connect((ip, port))
  while True:
    if not kill_received:
      response = sock.recv(1024)
      print "{}".format(response)
    else:
      sock.close()
      break

if __name__ == "__main__":
  client()
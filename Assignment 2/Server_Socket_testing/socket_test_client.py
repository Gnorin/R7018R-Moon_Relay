import socket
import time

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(('localhost', 10000))

clientsocket.send(b'spacecraft')

time.sleep(10)
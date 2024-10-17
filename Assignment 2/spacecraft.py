import socket
import time

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientsocket.connect(('localhost', 10000))
print("connected")

clientsocket.send(b'spacecraft')

time.sleep(3)

print("sending data...")
clientsocket.send(b'This is my data. I hope you like it.')

time.sleep(10)

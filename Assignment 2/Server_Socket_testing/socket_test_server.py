import socket
import threading
import time

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serversocket.bind(('localhost', 10000))

serversocket.listen(3)

def test_function(clientsocket : socket.socket):
    MSGLEN = len(clientsocket.recv(1)) # The first 8 bytes sent by the socket contains the length of the message as an unsigned int.
    chunks = []
    bytes_recd = 0
    while bytes_recd < MSGLEN:
        chunk = clientsocket.recv(min(MSGLEN - bytes_recd, 256))
        if chunk == b'':
            print("socket connection broken")
            break
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    print(chunks)
    time.sleep(5)

def command_line(clientsocket : socket.socket):
    while True:
        print(clientsocket)
        time.sleep(1)

def ground_station(clientsocket : socket.socket):
    while True:
        print(clientsocket)
        time.sleep(2)

def spacecraft(clientsocket : socket.socket):
    while True:
        print(clientsocket)
        time.sleep(3)

accepted_sockets = [
    b'command_line',
    b'ground_station',
    b'spacecraft',
]

threads = [
    # Threads will go here and start when all of the sockets have been initialised
]

# Main loop...
while True:
    # Accept incoming client sockets
    (clientsocket, address) = serversocket.accept()

    socket_type = clientsocket.recv(16)

    # Goes through the subsystems we are looking for, and matches them to subroutine sockets that handle the communication
    for subsystem_socket in accepted_sockets:
        if subsystem_socket[0] == socket_type:
            match socket_type:
                case b'command_line':
                    threads.append(threading.Thread(target=command_line(clientsocket=clientsocket)))
                case b'ground_station':
                    threads.append(threading.Thread(target=ground_station(clientsocket=clientsocket)))
                case b'spacecraft':
                    threads.append(threading.Thread(target=spacecraft(clientsocket=clientsocket)))
                case _:
                    print("Dont know how we got here...")
            break
    
    if len(threads) == 3:
        break

for thread in threads:
    thread.start()


def connect(my_socket, host, port):
    my_socket.sock.connect((host, port))

def mysend(self, msg):
    totalsent = 0
    MSGLEN = len(msg)
    self.sock.send(MSGLEN) # after determining the length of the message, we tell the socket listening how much data we will send
    while totalsent < MSGLEN:
        sent = self.sock.send(msg[totalsent:])
        if sent == 0:
            print("socket connection broken")
        totalsent = totalsent + sent

def myreceive(self):
    MSGLEN = self.sock.recv(8) # The first 8 bytes sent by the socket contains the length of the message as an unsigned int.
    chunks = []
    bytes_recd = 0
    while bytes_recd < MSGLEN:
        chunk = self.sock.recv(min(MSGLEN - bytes_recd, 256))
        if chunk == b'':
            print("socket connection broken")
        chunks.append(chunk)
        bytes_recd = bytes_recd + len(chunk)
    return chunks
import socket as soc
from socket import socket
from time import sleep

###############################################################################################################
### Configuration
###############################################################################################################
# Socket which will listen for and accept incoming sockets. 
terminal_socket = socket(soc.AF_INET, soc.SOCK_STREAM)

# Configures the accepted sockets. Format needs to be bytes to match with the returned data from the sockets.
accepted_sockets = None

address = 'localhost'   # Address used for our groundstation and spacecraft sockets.
port = 10000            # Port used for our groundstation socket.

###############################################################################################################
### Connecting to ground station
###############################################################################################################
is_connected = False
while is_connected == False:
    try:
        print("Connecting to ground station...")
        terminal_socket.connect((address, port))
        print(f"{address}:{port} - ground_station : connected")
        is_connected = True
    except:
        print("Ground station offline...")

terminal_socket.send(b'command_line')
sleep(0.1)

###############################################################################################################
### Main loop
###############################################################################################################
while True:
    command = input("Enter a command: ")

    terminal_socket.send(command.encode('utf-8'))
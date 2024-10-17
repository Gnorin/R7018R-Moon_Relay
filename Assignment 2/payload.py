import socket as soc
from socket import socket
from time import sleep

###############################################################################################################
### Configuration
###############################################################################################################
# Socket which will listen for and accept incoming sockets. 
payload_socket = socket(soc.AF_INET, soc.SOCK_STREAM)

# Configures the accepted sockets. Format needs to be bytes to match with the returned data from the sockets.
accepted_sockets = None

address = 'localhost'   # Address used for our groundstation and spacecraft sockets.
spaceport = 11000            # Port used for our groundstation socket.

payload_socket.connect(('localhost', spaceport))

payload_socket.send(b'payload')

sleep(10)
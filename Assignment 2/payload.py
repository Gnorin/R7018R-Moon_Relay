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


###############################################################################################################
### Initialisation
###############################################################################################################

# Connects to the spacecraft via spacewire B^)
print("Connecting to spacecraft...")
payload_socket.connect(('localhost', spaceport))
payload_socket.send(b'payload')
print("Success! Connected to spacecraft")

print("Booting up...")
sleep(5)

print("Entering main loop.")
# Main loop
while True:
    # Reads data from the spacecraft stream until a valid request is read.
    print("Listening for spacecraft request.")
    request = payload_socket.recv(4096)
    if request != b'':
        print("Incoming request...")

        request = request.decode('utf-8')

        i = 0
        for c in request:
            if c == ';':
                i0 = i
            elif c == ' ':
                request_command = request[i0+1:i]
                request_argument = request[i+1:]
                break
            i = i + 1
        
        i = 0
        for c in request_argument:
            if c == ' ':
                request_functionality = request_argument[:i]
                request_parameter = request_argument[i+1:]
                break
            i = i + 1

        sleep(1)

        if request_command == "tc_relay":
            print(f"Request accepted: relaying <{request_parameter}> to connected spacecraft")
            print("Sending...")
            sleep(10)
            print("Success")
            payload_socket.send(b'Success. Message relayed to spacecraft')
        else:
            print("Bad request")
            print(request_command)
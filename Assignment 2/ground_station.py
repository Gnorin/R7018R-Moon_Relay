import socket as soc
import threading
from socket import socket
from threading import Thread
from time import sleep

###############################################################################################################
### Configuration
###############################################################################################################
# Socket which will listen for and accept incoming sockets. 
serversocket = socket(soc.AF_INET, soc.SOCK_STREAM)

# Configures the accepted sockets. Format needs to be bytes to match with the returned data from the sockets.
accepted_sockets = [
    b'command_line',
    b'spacecraft'
]

address = 'localhost'   # Address used for our groundstation and spacecraft sockets.
port = 10000            # Port used for our groundstation socket.
spaceport = 11000       # Port used for our spacecraft socket.


###############################################################################################################
### Subroutines for communication between the ground station and the spacecraft, and the command_line window
###############################################################################################################

# command_line_input(clientsocket : socket) is designed to receive commands through a socket from the command_line.
# This function handles telecommands received from the command line socket and checks if that sent telecommand is valid in our MIB
def command_line_input(clientsocket : socket):
    global active_sockets
    thread_id = threading.current_thread().name
    is_thread_alive = True
    while is_thread_alive == True:
        telecommand = clientsocket.recv()
        
        # Check telecommand here, if the telecommand is valid, add it to the pile of telecommands.        
        telecommands.append(telecommand)

        # Checks if the thread is still alive, and effectively terminates it doesn't exist anymore.
        for active_socket in active_sockets:
            if active_socket[1] == thread_id:
                break
        else:
            return


# spacecraft_downlink(clientsocket : socket) is designed to receive data through a socket from the spacecraft.py script.
def spacecraft_downlink(clientsocket : socket):
    global active_sockets
    thread_id = threading.current_thread().name
    is_thread_alive = True
    while is_thread_alive == True:
        data = clientsocket.recv(4096)
        if data != b'':
            # This section has to be fleshed out to support proper data downlink.
            print(f"here is the data: {data}")
            spacecraft_data.append(data)
        
        # Checks if the thread is still alive, and effectively terminates it doesn't exist anymore.
        for active_socket in active_sockets:
            if active_socket[1] == thread_id:
                break
        else:
            return


# The subroutines which are initiated by incoming sockets.
subroutines = [
    (b'command_line', command_line_input),
    (b'spacecraft', spacecraft_downlink)
]

# The subroutines which are initiated by this ground station
def spacecraft_uplink(spacecraft_socket : socket):
    global telecommands
    while True:
        nr_of_sent_commands = 0
        for telecommand in telecommands:
            spacecraft_socket.send(telecommand)
            nr_of_sent_commands += 1

        # Erases the previous sent telecommands
        telecommands = telecommands[nr_of_sent_commands:]



###############################################################################################################
### Socket handling
###############################################################################################################

# accept_sockets() is designed to accept incoming sockets, and sort out bad requests.
# This function appends valid sockets to the list active_sockets
def accept_sockets():
    global active_sockets

    # Accept incoming client sockets
    (clientsocket, address) = serversocket.accept()
    connection = clientsocket.recv(16) # We arbitrarily decided to read 16 bytes, as the longest accepted socket name is less than 16 bytes.

    # Checks that the socket trying to connect is in the list of accepted connections
    for socket in accepted_sockets:
        if connection == socket:
            # If a socket by that name already exists, then that socket terminated and a new one is trying to connect.
            if len(active_sockets) > 0:
                index = 0
                for active_socket in active_sockets:
                    if connection == active_socket[0]:
                        active_sockets = active_sockets[:index] + active_sockets[index+1:]
                        print(f"\nError:\t{connection.decode('utf-8')} : terminated")
                        break
                    index += 1
            new_sockets.append((connection, clientsocket))
            print(f"\n{address[0]}:{address[1]} - {connection.decode('utf-8')} : connected")
            break
    else:
        print(f"Error:\tSocket did not match any accepted sockets: {connection}")
    return


# start_communication(new_socket) is designed to dispatch threads which handle the communication between connected sockets.
def start_communication(new_socket):
    global subroutines

    # Goes through the subsystems we are looking for, and matches them to subroutine sockets that handle the communication
    for subroutine in subroutines:
        if subroutine[0] == new_socket[0]:
            subroutine_thread = Thread(target=subroutine[1], args=(new_socket[1],))
            active_sockets.append((new_socket[0], subroutine_thread.name))
            subroutine_thread.start()
            break
    else:
        print(f"Error:\tUnable to match new_socket='{new_socket[0]}' to case.")
    return 0



###############################################################################################################
### Initialisation
###############################################################################################################

# Makes our socket listen for connections, making it a server socket.
serversocket.bind((address, port))
serversocket.listen(2)



###############################################################################################################
### Main loop. This loop dispatches threads to handle the communication between sockets
###############################################################################################################

# A list of current commands which are being handled in the main loop.
telecommands = [b"tc_relay configure id=404"]

# The data received from the spacecraft
spacecraft_data = []

# A list of the currently active sockets.
active_sockets = []

# A list of newly made sockets.
new_sockets = []

# Thread which will handle the incoming sockets.
accept_sockets_thread = Thread()

# Socket and thread which will send telecommands to the spacecraft.
spacecraft_socket = socket(soc.AF_INET, soc.SOCK_STREAM)
send_telecommands_thread = Thread()

while True:
    # Continue accepting new sockets.
    if accept_sockets_thread.is_alive() == False:
        # Makes a new thread to run on the next iteration.
        accept_sockets_thread = Thread(target=accept_sockets)
        accept_sockets_thread.start()
    
    # When there are any new sockets, start them on a new thread.
    nr_of_new_sockets = 0
    for new_socket in new_sockets:
        start_communication(new_socket)
        nr_of_new_sockets += 1
    new_sockets = new_sockets[nr_of_new_sockets:]

    # Continue sending new telecommands
    if send_telecommands_thread.is_alive() == False:
        # Makes a new thread to run on the next iteration.
        send_telecommands_thread = Thread(target=spacecraft_uplink, args=(spacecraft_socket,))
        try:
            spacecraft_socket.connect((address, spaceport)) # Connects to the spacecraft
            active_sockets.append((b'ground_station', send_telecommands_thread.name)) # Adds it to the list of active sockets
            spacecraft_socket.send(b'ground_station') # Specifies that this is the ground_station
            sleep(0.1)
            send_telecommands_thread.start()
        except:
            print("Connection to spacecraft failed.")
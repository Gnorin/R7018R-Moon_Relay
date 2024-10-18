import socket as soc
import threading
from socket import socket
from threading import Thread
from time import sleep
from read_TC import read_TC
from OBSW_functions import pacman, unpacman, verify_TM, tc_relay, housekeeping, housekeeping_TM, mode, attitude, star_tracker, battery_kill, schedule, send_TM, TM_id, TC_id, housekeeping_config, tc_relay_config, mode_config, attitude_config, star_tracker_config, battery_kill_config, schedule_config
from BIM import BIM
from random import randint

###############################################################################################################
### Configuration
###############################################################################################################
# Socket which will listen for and accept incoming sockets. 
serversocket = socket(soc.AF_INET, soc.SOCK_STREAM)

# Configures the accepted sockets. Format needs to be bytes to match with the returned data from the sockets.
accepted_sockets = [
    b'ground_station',
    b'payload'
]

address = 'localhost'   # Address used for our groundstation and spacecraft sockets.
port = 10000            # Port used for our groundstation socket.
spaceport = 11000       # Port used for our spacecraft socket.



###############################################################################################################
### Subroutines for communication between the ground station and the spacecraft, and the command_line window
###############################################################################################################

def spacecraft_uplink(clientsocket : socket):
    global active_sockets
    global telecommands
    thread_id = threading.current_thread().name
    is_thread_alive = True
    connection = b'ground_station'
    try:
        while is_thread_alive == True:
            telecommands.append(clientsocket.recv(4096))
            if telecommands != []:
                for telecommand in telecommands:
                    read_flag = read_TC(unpacman(telecommand))
                    functionality = read_flag[0]
                    argument = read_flag[1]
                    data = read_flag[2]
                    TC.index = TC.index+1
                    verify_pac = verify_TM(TC,TM,functionality,argument,data)
                    telemetry.append(verify_pac[1])
                    if verify_pac[0] == 1:
                        match functionality:
                            case "tc_relay":
                                data_return =  tc_relay(argument,data,tc_relay_configuration)
                            case "housekeeping":
                                data_return = housekeeping(argument,data,housekeeping_configuration)
                            case "mode":
                                data_return = mode(argument,data,mode_configuration)
                            case "attitude":
                                data_return = attitude(argument,data,attitude_configuration, mode_configuration)
                            case "star_tracker":
                                data_return = star_tracker(argument,data,star_tracker_configuration,mode_configuration)
                            case "battery_kill":
                                data_return = battery_kill(argument,data,battery_kill_configuration)
                            case "schedule":
                                data_return = schedule(argument,data,schedule_configuration)
                            case _:
                                data_return = 0
                    #Code to check if something needs to be sent
                        if data_return != 0:
                            telemetry.append(send_TM(data_return, data, TM))
                telecommands = []

            # Checks if the thread is still alive, and effectively terminates it if it doesn't exist anymore.
            for active_socket in active_sockets:
                if active_socket[1] == thread_id:
                    break
            else:
                return
    except:
        index = 0
        for active_socket in active_sockets:
            if connection == active_socket[0]:
                active_sockets = active_sockets[:index] + active_sockets[index+1:]
                print(f"\nError:\t{connection.decode('utf-8')} : terminated")
                return
            index += 1

def payload_downlink(clientsocket : socket):
    global active_sockets
    thread_id = threading.current_thread().name
    is_thread_alive = True
    connection = b'payload'
    try:
        while is_thread_alive == True:
            data = clientsocket.recv(4096)
            if data != b'':
                # This section has to be fleshed out to support proper data downlink.
                print(f"here is the payload data: {data}")
                payload_data.append(data)

            # Checks if the thread is still alive, and effectively terminates it if it doesn't exist anymore.
            for active_socket in active_sockets:
                if active_socket[1] == thread_id:
                    break
            else:
                return
    except:
        index = 0
        for active_socket in active_sockets:
            if connection == active_socket[0]:
                active_sockets = active_sockets[:index] + active_sockets[index+1:]
                print(f"\nError:\t{connection.decode('utf-8')} : terminated")
                return
            index += 1

# The subroutines which are initiated by an incoming socket
subroutines = [
    (b'ground_station', spacecraft_uplink),
    (b'payload', payload_downlink)
]

# The subroutines which are initiated by this spacecraft
def spacecraft_downlink(clientsocket : socket):
    global active_sockets
    global telemetry
    thread_id = threading.current_thread().name
    is_thread_alive = True
    connection = b'spacecraft'
    try:
        while is_thread_alive == True:
            if telemetry != []:
                clientsocket.send(telemetry[0])
                telemetry = telemetry[1:]

            sleep(telemetry_period)

            # Checks if the thread is still alive, and effectively terminates it if it doesn't exist anymore.
            for active_socket in active_sockets:
                if active_socket[1] == thread_id:
                    break
            else:
                return
    except:
        index = 0
        for active_socket in active_sockets:
            if connection == active_socket[0]:
                active_sockets = active_sockets[:index] + active_sockets[index+1:]
                print(f"\nError:\t{connection.decode('utf-8')} : terminated")
                return
            index += 1



###############################################################################################################
### Other subroutines: Cyclic housekeeping, reading main obc temperature, reading the battery charge, and
### reading pressure data
###############################################################################################################

def cyclic_housekeeping():
    thread_id = threading.current_thread().name
    is_thread_alive = True
    while is_thread_alive == True:
        read_temperature()
        read_pressure()
        read_battery_charge()

        hk = housekeeping_TM(TM, housekeeping_configuration, str(temperature_data), str(pressure_data), str(battery_data))
        if hk != "":
            housekeeping_log.append(hk)
        
        telemetry.append(hk)

        sleep(housekeeping_configuration.log_period)
        
        # Checks if the thread is still alive, and effectively terminates it if it doesn't exist anymore.
        for local_thread in local_threads:
            if local_thread == thread_id:
                break
        else:
            return

def read_temperature():
    global temperature_data
    if housekeeping_configuration.temp != -1:
        temperature_data = randint(55, 65) # Given in degrees Celcius

def read_pressure():
    global pressure_data
    if housekeeping_configuration.pressure != -1:
        pressure_data = randint(2000, 4000) * (10 ** (-14)) # Pressure given in Pascal

def read_battery_charge():
    global battery_data
    if housekeeping_configuration.battery != -1: # This is a bit unrealistic, but we only consume battery when
        battery_data -= randint(0, 10)/10        # we read from the batteries. Indeed, one might call it schrödingers battery

###############################################################################################################
### Socket handling
###############################################################################################################

# accept_sockets() is designed to accept incoming sockets, and sort out bad requests.
# This function appends valid sockets to the list active_sockets
def accept_sockets():
    global active_sockets

    # Accept incoming client sockets
    (clientsocket, address) = serversocket.accept()
    connection = clientsocket.recv(16)  # We arbitrarily decided to read 16 bytes, as the longest accepted
                                        # socket name is less than 16 bytes.

    # Checks that the socket trying to connect is in the list of accepted connections
    for socket in accepted_sockets:
        if connection == socket:
            # If a socket by that name already exists, then that socket terminated and a new one is trying
            # to connect.
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


# start_communication(new_socket) is designed to dispatch threads which handle the communication between
# connected sockets.
def start_communication(new_socket):
    global subroutines
    # Goes through the subsystems we are looking for, and matches them to subroutine sockets that handle
    # the communication
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
serversocket.bind((address, spaceport))
serversocket.listen(2)



###############################################################################################################
### Main loop. This loop dispatches threads to handle the communication between sockets
###############################################################################################################

# A list of current commands which are being handled in the main loop.
telecommands = []

# A list of current commands which are being handled in the main loop.
telemetry = []

# The variable controlling how often we send telemetry
telemetry_period = 1

# A list of payload data
payload_data = []

# The TM class used for keeping track of the currently sent TM
TM = TM_id()
TM.index = 0
TM.type = 'TM'

# The TC class used for keeping track of the currently sent TC
TC = TC_id()
TC.index = 0
TC.type = 'TC'
TC.expected = TC.index + 1

temperature_data = 15           # Degrees Celcius
battery_data = 100              # % Charge remaining
pressure_data = 3*(10**(-11))   # Pascal

housekeeping_configuration = housekeeping_config() #1

housekeeping_log = []

tc_relay_configuration = tc_relay_config() #2

mode_configuration = mode_config() #3

attitude_configuration = attitude_config() #4

star_tracker_configuration = star_tracker_config() #5

battery_kill_configuration = battery_kill_config() #6

schedule_configuration = schedule_config() #7

# A list of the currently active sockets.
active_sockets = []

# A list of newly made sockets. The sockets are made in the accept_sockets() function, and then moved to the
# active_sockets list in the main loop using the start_communication() function.
new_sockets = []

# Thread which will handle the incoming sockets.
accept_sockets_thread = Thread()

# Socket and thread which will send telecommands to the spacecraft.
ground_station_socket = socket(soc.AF_INET, soc.SOCK_STREAM)
send_telemetry_thread = Thread()

# A list of threads which dont have socket clients attached.
local_threads = []

# Housekeeping thread.
housekeeping_thread = Thread()

while True:
    ### Socket code
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

    # Continue sending new telemetry
    if send_telemetry_thread.is_alive() == False:
        # Makes a new thread to run on the next iteration.
        send_telemetry_thread = Thread(target=spacecraft_downlink, args=(ground_station_socket,))
        try:
            ground_station_socket.connect((address, port)) # Connects to the ground_station
            active_sockets.append((b'spacecraft', send_telemetry_thread.name)) # Adds it to the list of active sockets
            ground_station_socket.send(b'spacecraft') # Specifies that it is the spacecraft
            sleep(0.1) # Slight delay to enable the ground station to finish reading the message
            send_telemetry_thread.start()
        except:
            index = 0
            for active_socket in active_sockets:
                if b'spacecraft' == active_socket[0]:
                    active_sockets = active_sockets[:index] + active_sockets[index+1:]
                    print(f"\nError:\tspacecraft : terminated")
                    break
                index += 1
            print("Connection to ground station failed.")
    

    ### Cyclic housekeeping code
    if housekeeping_thread.is_alive() == False:
        index = 0
        for local_thread in local_threads:
            if local_thread == housekeeping_thread.name:
                local_threads = local_threads[:index] + local_threads[index+1:]
                break
            index += 1

        housekeeping_thread = Thread(target=cyclic_housekeeping)
        local_threads.append(housekeeping_thread.name)
        housekeeping_thread.start()

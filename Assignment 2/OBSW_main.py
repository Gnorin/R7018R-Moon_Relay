
import OBSW_functions
import read_TC
import BIM


#0 is error. 1 is usage, 2 is config.

command_list = BIM.BIM

class housekeeping_config:
    on_off = 0
    temp = 1
    pressure = 1
    battery = 1

class tc_relay_config:
    id = 0
    br = 0
    send_flag = 0

class mode_config:
    mode = "OFF"

class attitude_config:
   yaw_pitch_roll = "00.0 00.0 00.0"

class star_tracker_config:
    on = 0
    off = 1
    freq_res_fov = "00.0 00.0 00.0"

class battery_kill_config:
    code = "self-destruct"
    killed = 0

class schedule_config:
    schedule_list = []
    #MUST USE FORMAT OF 00:00 FOLLOWED BY COMMAND

class TM_id:
    index = 0
    type = "TM"

class TC_id:
    index = 0
    type = "TC"
    expected = index+1

housekeeping_configuration = housekeeping_config() #1

tc_relay_configuration = tc_relay_config() #2

mode_configuration = mode_config() #3

attitude_configuration = attitude_config() #4

star_tracker_configuration = star_tracker_config() #5

battery_kill_configuration = battery_kill_config() #6

schedule_configuration = schedule_config() #7

id_TM = TM_id()

id_TC = TC_id()


temperature_data = "temp1"
battery_data = "battery1"
pressure_data = "pressure1"

while True:

    
    data_return = 0
    print("Enter Input\r")
    tc = input()
    print("\r")
    read_flag = read_TC.read_TC(tc)

    if read_flag == 0:
        print("INVALID TC")
    else:
        functionality = read_flag[0]
        argument = read_flag[1]
        data = read_flag[2]
        id_TC.index = id_TC.index+1
        verify_pac = OBSW_functions.verify_TM(id_TC,id_TM,functionality,argument,data)
        print(verify_pac[1]) #THIS IS THE VALUE FOR THE VERIFY PACKET
        if verify_pac[0] == 1:
            match functionality:
                case "tc_relay":
                    data_return =  OBSW_functions.tc_relay(argument,data,tc_relay_configuration)
                case "housekeeping":
                    data_return = OBSW_functions.housekeeping(argument,data,housekeeping_configuration)
                case "mode":
                    data_return = OBSW_functions.mode(argument,data,mode_configuration)
                case "attitude":
                    data_return = OBSW_functions.attitude(argument,data,attitude_configuration, mode_configuration)
                case "star_tracker":
                    data_return = OBSW_functions.star_tracker(argument,data,star_tracker_configuration,mode_configuration)
                case "battery_kill":
                    data_return = OBSW_functions.battery_kill(argument,data,battery_kill_configuration)
                case "schedule":
                    data_return = OBSW_functions.schedule(argument,data,schedule_configuration)
                case _:
                    data_return = 0
        #Code to check if something needs to be sent
            if data_return != 0:
                send_data = OBSW_functions.send_TM(data_return,data,id_TM)

    #Housekeeping command
    hk = OBSW_functions.housekeeping_TM(id_TM, housekeeping_configuration, temperature_data, pressure_data, battery_data)
    if hk != "":
        print(hk)
    





    
    








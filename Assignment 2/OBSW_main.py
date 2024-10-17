
import OBSW_functions
import read_TC
import BIM


#0 is error. 1 is usage, 2 is config.

command_list = BIM.BIM

class housekeeping_config:
    temp = 0
    pressure = 0
    battery = 0

class tc_relay_config:
    id = 0
    br = 0
    send_flag = 0

class mode_config:
    OFF = 1
    INITIAL = 0
    SAFE = 0
    NOMINAL = 0
    MANOUEVER = 0

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
    schedule_list = [""]
    #MUST USE FORMAT OF 00:00 FOLLOWED BY COMMAND


housekeeping_configuration = housekeeping_config()

tc_relay_configuration = tc_relay_config()

mode_configuration = mode_config()

attitude_configuration = attitude_config()

star_tracker_configuration = star_tracker_config()

battery_kill_configuration = battery_kill_config()

schedule_configuration = schedule_config()

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
                print("Unexpected")
    print(data_return)








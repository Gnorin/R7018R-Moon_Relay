


class housekeeping_config:
    temp = 0
    pressure = 0
    battery = 0
    on_off = 0


class mode_config:
    OFF = 1
    INITIAL = 0
    SAFE = 0
    NOMINAL = 0
    MANOUEVER = 0

class attitude_config:
    yaw_pitch_roll = "00.0 00.0 00.0"

class tc_relay_config:
    id = 0
    br = 0
    send_flag = 0

class star_tracker_config:
    on = 0
    off = 1
    freq_res_fov = "00.0 00.0 00.0"

class schedule_config:
    schedule_list = [""]
    #MUST USE FORMAT OF 00:00 FOLLOWED BY COMMAND

class battery_kill_config:
    code = "self-destruct"
    killed = 0

def tc_relay(argument, data, tc_relay_configuration : tc_relay_config):

    
    match argument:
        case "send":
            tc_relay_configuration.send_flag = 1     
            return 1
        case "configure":
            if len(data) >=4:
                match data[0:2]:
                    case "id":
                        tc_relay_configuration.id = data[3:len(data)]
                        return 1
                    case "br":
                        tc_relay_configuration.br = data[3:len(data)]
                        return 1
            else:
                return 0

    return 0


def housekeeping(argument,data, housekeeping_configuration : housekeeping_config):
    
    match argument:
        case "on":
            housekeeping_configuration.on_off = 1
            return 1 
        case "off":
            housekeeping_configuration.on_off = 0     
            return 1
        case "configure":
            match data:
                case "temperature":
                    housekeeping_configuration.temp = housekeeping_configuration.temp*-1   
                    return 1      
                case "battery":
                    housekeeping_configuration.battery = housekeeping_configuration.battery*-1 
                    return 1
                case "temperature":
                    housekeeping_configuration.pressure = housekeeping_configuration.pressure*-1 
                    return 1
                case _:
                    return 0
        case _:
            return 0
               
            

    




def mode(argument,data,mode_configuration : mode_config):


    match argument:
        case"change":
            match data:
                case "SAFE":
                    mode_configuration.OFF = 0
                    mode_configuration.INITIAL = 0
                    mode_configuration.SAFE = 1
                    mode_configuration.NOMINAL = 0
                    mode_configuration.MANOUEVER = 0
                    return 1
                case "NOMINAL":
                    mode_configuration.OFF = 0
                    mode_configuration.INITIAL = 0
                    mode_configuration.SAFE = 0
                    mode_configuration.NOMINAL = 1
                    mode_configuration.MANOUEVER = 0
                    return 1
                case "MANOUEVER":
                    mode_configuration.OFF = 0
                    mode_configuration.INITIAL = 0
                    mode_configuration.SAFE = 0
                    mode_configuration.NOMINAL = 0
                    mode_configuration.MANOUEVER = 1
                    return 1
                case _:
                    return 0
        case "check":
            if mode_configuration.INITIAL == 1:
                return "INITIAL"
            elif mode_configuration.SAFE == 1:
                return "SAFE"
            elif mode_configuration.NOMINAL == 1:
                return "NOMINAL"
            elif mode_configuration.MANOUEVER == 1:
                return "MANOUEVER"
            else:
                return 0


def attitude(argument,data, attitude_configuration : attitude_config, mode_configuration : mode_config):
    if mode_configuration.MANOUEVER != 1:
        return 0
    else:
        match argument:
            case "get":
                return [attitude_configuration.yaw_pitch_roll]
            case "change":
                attitude_configuration.yaw_pitch_roll = data
                return 1
            case _:
                return 0


    return 0
def star_tracker(argument,data, star_tracker_configuration : star_tracker_config, mode_configuration : mode_config):

    if mode_configuration.NOMINAL != 1:
        return 0
    else:
        match argument:
            case "on":
                star_tracker_configuration.on = 1
                star_tracker_configuration.off = 0
                return 1
            case "off":
                star_tracker_configuration.on = 0
                star_tracker_configuration.off = 1
                return 1
            case "configure":
                star_tracker_configuration.freq_res_fov = data
                return 1
            case _:
                return 0
            

    return 0
def schedule(argument,data,schedule_configuration : schedule_config):

    match argument:
            case "command":
                schedule_configuration.schedule_list.append(data)
                return 1
            case "clear":
                schedule_configuration.schedule_list = [" "]
                return 1
            case "check":
                return schedule_configuration.schedule_list
            case _:
                return 0


    return 0
def battery_kill(argument,data, battery_kill_configuration : battery_kill_config):
    
    match argument:
        case "command":
            if data == battery_kill_configuration.code:
                print("goodnite sweet prince")
                battery_kill_configuration.killed = 1
                return 1
            else:
                print("No such known command")
                return 1
        case _:
            return 0


    return 0

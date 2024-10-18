


class housekeeping_config:
    temp = 1
    pressure = 1
    battery = 1
    on_off = 1
    log_period = 5


class mode_config:
    mode = "OFF"

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

class TM_id:
    index = 0
    type = "TM"

class TC_id:
    index = 0
    type = "TC"
    expected = index+1

def tc_relay(argument, data, tc_relay_configuration : tc_relay_config):#2

    
    match argument:
        case "send":
            tc_relay_configuration.send_flag = 1     
            return [2,1]
        case "configure":
            if len(data) >=4:
                match data[0:2]:
                    case "id":
                        tc_relay_configuration.id = data[3:len(data)]
                        return [2,2]
                    case "br":
                        tc_relay_configuration.br = data[3:len(data)]
                        return [2,2]
            else:
                return 0

    return 0


def housekeeping(argument,data, housekeeping_configuration : housekeeping_config):#1
    
    match argument:
        case "on":
            housekeeping_configuration.on_off = 1
            return [1,1] 
        case "off":
            housekeeping_configuration.on_off = 0     
            return [1,2]
        case "configure":
            match data:
                case "temperature":
                    housekeeping_configuration.temp = housekeeping_configuration.temp*(-1)   
                    return [1,3]      
                case "battery":
                    housekeeping_configuration.battery = housekeeping_configuration.battery*(-1) 
                    return [1,3]    
                case "temperature":
                    housekeeping_configuration.pressure = housekeeping_configuration.pressure*(-1) 
                    return [1,3]    
                case _:
                    return 0
        case _:
            return 0
               
            

    




def mode(argument,data,mode_configuration : mode_config):#3


    match argument:
        case"change":
            match data:
                case "SAFE":
                    mode_configuration.mode = "SAFE"
                    return [3,1]
                case "NOMINAL":
                    mode_configuration.mode = "NOMINAL"
                    return [3,1]
                case "MANOUEVER":
                    mode_configuration.mode = "MANOUEVER"
                    return [3,1]
                case _:
                    return 0
        case "check":
                return [3,1,1]
        case _:
            return 0


def attitude(argument,data, attitude_configuration : attitude_config, mode_configuration : mode_config):#4
    if mode_configuration.mode != "MANOUEVER":
        return [40,40]
    else:
        match argument:
            case "get":
                data = attitude_configuration.yaw_pitch_roll
                return [[4,1,1],[data],[1]]
            case "change":
                attitude_configuration.yaw_pitch_roll = data
                return [4,2]
            case _:
                return 0


    return 0
def star_tracker(argument,data, star_tracker_configuration : star_tracker_config, mode_configuration : mode_config):#5

    if mode_configuration.mode != "NOMINAL":
        return [40,40]
    else:
        match argument:
            case "on":
                star_tracker_configuration.on = 1
                star_tracker_configuration.off = 0
                return [5,1]
            case "off":
                star_tracker_configuration.on = 0
                star_tracker_configuration.off = 1
                return [5,2]
            case "configure":
                star_tracker_configuration.freq_res_fov = data
                return [5,2]
            case _:
                return 0
            

    return 0
def schedule(argument,data,schedule_configuration : schedule_config):#7

    match argument:
            case "command":
                schedule_configuration.schedule_list.append(data)
                return [7,1]
            case "clear":
                schedule_configuration.schedule_list = [" "]
                return [7,2]
            case "check":
                a = 0
                data = ""
                while a < len(schedule_configuration.schedule_list):
                    data = str(a)+":"+data+schedule_configuration.schedule_list[a]+":::"
                    a= a+1
                return [[7,3,1],[data],[1]]
            case _:
                return 0


    return 0
def battery_kill(argument,data, battery_kill_configuration : battery_kill_config):#6
    
    match argument:
        case "command":
            if data == battery_kill_configuration.code:
                print("goodnite sweet prince")
                battery_kill_configuration.killed = 1
                return [6,1]
            else:
                
                return [6,2]
        case _:
            return 0


    return 0


#TC/TM FUNCTIONS

def pacman(command, id : TM_id):
    
    
    TM_string_uncoded = id.type + str(id.index)+";"+command


    



    return TM_string_uncoded.encode('utf-8')

def unpacman(TC):
#returns id and command seperately
#Commands are setup like TCid;"command"
    TC = TC.decode('utf-8')
    a = 0
    while a < len(TC):
        if TC[a] == ";":
            return[TC[0:a],TC[a:len(TC)]] 
        a=a+1
    return 0
            
        
    


#TM functions

def housekeeping_TM(id : TM_id, housekeeping_configuration : housekeeping_config, temperature_data, pressure_data, battery_data):
    housekeeping_TM = ""
    if housekeeping_configuration.on_off == 1:
        if housekeeping_configuration.temp == 1:
            housekeeping_TM = housekeeping_TM + temperature_data
        if housekeeping_configuration.pressure == 1:
            housekeeping_TM = housekeeping_TM + " " + pressure_data
        if housekeeping_configuration.battery == 1:
            housekeeping_TM = housekeeping_TM + " " + battery_data
        return_data = pacman(housekeeping_TM,id)
        id.index = id.index +1
    else:
        return_data=""
    
    return return_data

def verify_TM(id_TC : TC_id, id_TM: TM_id, functionality, argument, data):
    if id_TC.index == id_TC.expected:
        send_TM = pacman(id_TC.type +str(id_TC.index) + ";" +functionality+" " +argument + " " +data + "; OK", id_TM)
        id_TM.index = id_TM.index +1
        id_TC.expected = id_TC.index +1
        return[1,send_TM]
    else:
        send_TM = pacman(id_TC.type +str(id_TC.index) + ";" +functionality+" " + +argument + "" +data + "; DENIED: EXPECTED: " +id_TC.type + str(id_TC.expected), id_TM)
        id_TM.index = id_TM.index +1
        return[0,send_TM]
    

def send_TM(data_return, data, id_TM : TM_id):
    

    if  len(data_return) == 2:
        if data_return[0] == 40 and data_return[1] == 40:
            return_data= pacman(data + "; WRONG MODE; DENIED",id_TM)
            id_TM.index == id_TM.index+1
            return return_data
        else:
            return 0
        
    elif len(data_return[0]) == 3:
        return_data = pacman(data_return[1][0],id_TM)
        id_TM.index == id_TM.index+1
        return return_data
   


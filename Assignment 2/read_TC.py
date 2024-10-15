import check_TC
import OBSW_functions

input = "housekeeping configure data"



def read_TC(input):
    
    
    r1 = 0
    c1 = -1
    c2 = 0

    while r1 < len(input):
        
        if input[r1] == ' ' and c1 == -1:
            c1 = r1
        elif input[r1] == ' ':
            c2 = r1
            break
        r1 = r1+1


    function_input = input[0:c1]
    argument_input = input[c1+1:c2]
    data_input = input[c2+1:len(input)]
    


    if check_TC.check_TC(function_input,argument_input) == 1:

        match function_input:
            case "tc_relay":
                OBSW_functions.tc_relay(argument_input,data_input)   
            case "housekeeping":
                OBSW_functions.housekeeping(argument_input,data_input)   
            case 'mode':
                OBSW_functions.mode(argument_input,data_input)   
            case 'attitude':
                OBSW_functions.attitude(argument_input,data_input)   
            case 'star_tracker':
                OBSW_functions.star_tracker(argument_input,data_input)   
            case 'scheduele':
                OBSW_functions.schedule(argument_input,data_input)   
            case 'battery_kill':
                OBSW_functions.battery_kill(argument_input,data_input)
            case _:
                print("Unexpected")
    else:
        print("Invalid TC")
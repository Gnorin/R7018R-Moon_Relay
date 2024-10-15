import BIM
command_list = BIM.BIM

input = "housekeeping configure data"



#Gotta divide it up into commands first

def check_TC(input):
    

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
    print(function_input)
    print(argument_input)
    print(data_input)

    function_valid_flag = False

    i1 = len(command_list)
    a = 0

    #Step 1: Look for function name first
    while a < i1+1:
        if command_list[a][0] == function_input:
                print("Found Function")
                
                function_valid_flag = True
                break
        else:
            
            a=a+1

    argument_valid_flag = False

    #Step 2: Look for argument
    i1 = a
    i2 = len(command_list[a][1])
    print(i2)
    a = 0
    while a < i2:
        if command_list[i1][1][a] == argument_input:
                print("Found Argument")
                argument_valid_flag = True
                break
        else:
            
            a=a+1

    if function_valid_flag == True and argument_valid_flag == True:
         
        return 0


check_TC(input)
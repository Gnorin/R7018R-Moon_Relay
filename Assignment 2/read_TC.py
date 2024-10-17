import BIM
command_list = BIM.BIM







def read_TC(input):
    #Divides the input into Function, argument and data
    if type(input) != type(" "):
        print("Not a string")
        return 0
    else:
        cut1 = -1

    cut1 = -1
    cut2= -1
    i1 = 0


    while i1 < len(input):
        if input[i1] == " " and cut1 == -1:
            cut1 = i1
        elif input[i1] == " " and cut2 == -1:
            cut2 = i1
        else:
            i1 = i1
        i1 = i1 +1


    functionality = input[0:cut1]
    argument = input[cut1+1:cut2]
    data = input[cut2+1:len(input)]
    
    #check if the functionality and argument exists

    functionality_flag = False
    argument_flag = False
    b = 0
    c = 0
    
    while b < len(command_list):
        if functionality == command_list[b][0]:
            
            functionality_flag = True
            break
        else:
            b = b+1

    
    if b < 7:
        while c < len(command_list[b][1]):
            if argument == command_list[b][1][c]:
                
                argument_flag = True
                break
            else:
                c = c+1
    else:
        functionality_flag = False


    if functionality_flag + argument_flag == 2:
        return[functionality,argument,data]
    else:
        return 0



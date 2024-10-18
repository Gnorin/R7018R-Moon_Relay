from threading import Thread
from time import sleep

class box:
    a = 0
    b = 0

def okay(mes, lis : box):
    for a in range(3):
        print(f"doing thread things..... {mes}")
        sleep(1)
    lis.a = 2
    return 0

a = box()

t = Thread(target=okay, args=("did it work?", a))


while True:
    print(f"doing other, very important, stuff :) Also, this is a: {a.a}")
    if t.is_alive() == False:
        t = Thread(target=okay, args=("did it work?", a))
        t.start()
    sleep(2)
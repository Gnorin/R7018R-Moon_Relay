import threading 
import time



iolock = threading.Lock()
  
def print_program():
  for i in range(20):
    iolock.release()
    time.sleep(1)
    
    print("Program")
    iolock.acquire()
  
def print_tryout(): 
      while True:
        iolock.acquire()
        data = input() 
        print(data)
        iolock.release()

t1 = threading.Thread(target=print_program)  
t2 = threading.Thread(target=print_tryout)  
t1.start()
t2.start()





from queue import Queue 
from threading import Thread 

import time
  
# A thread that produces data 
def producer(out_q, base): 
    for i in range(5): 
        # Produce some data 
        time.sleep(1)
        out_q.put(base ** i) 
          
# A thread that consumes data 
def consumer(in_q): 
    while True: 
        # Get some data 
        data = in_q.get() 
        # Process the data 
        print(data)
        # Indicate completion 
        in_q.task_done() 
          
# Create the shared queue and launch both threads 
q = Queue() 
t1 = Thread(target = consumer, args =(q, )) 
t2 = Thread(target = producer, args =(q, 2)) 
t3 = Thread(target = producer, args =(q, 3)) 
t1.start() 
t2.start() 
t3.start() 
  


print("end of code")
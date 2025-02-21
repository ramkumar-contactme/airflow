from threading import Thread,current_thread
from time import sleep,time
import queue
from simpleping import isup

THREADCOUNT = 5

f=open("ips.txt","r")
myq = queue.Queue()

for ip in f:
    myq.put(ip.strip()) 

f.close()

def worker():
    while not myq.empty():
        ip = myq.get()
        print(current_thread().name,ip,isup(ip))

threads = []
start = time()

#create and store threads in a list
for x in range(THREADCOUNT):
    t = Thread(target=worker)
    threads.append(t)

#start all the threads
for mythread in threads:
    print("Starting",mythread.name)
    mythread.start()

#wait for all the threads to finish  
for mythread in threads:
    mythread.join()
    print("Joining",mythread.name)

print("All threads finished executing")

end = time()
print(end - start)

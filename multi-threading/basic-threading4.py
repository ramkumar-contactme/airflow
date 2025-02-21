import queue, threading

myq = queue.Queue()

for i in range(100):
    myq.put(i)

def task():
    print(threading.current_thread().name, "has started")
    while not myq.empty():
        number = myq.get()
        print(number, number **2)
    print(threading.current_thread().name, "has ended")

thread_count=2
threads=[]

#Create threads
for i in range(thread_count):
    print(f"Creating Thread{i}")
    t=threading.Thread(target=task, name = f"Thread-{i}")
    threads.append(t)

#Start Threads
for mythread in threads:
    mythread.start()
#Wait for threads to finish
for mythread in threads:
    mythread.join()
print("Done")

import time
from threading import Thread

def hello():
    print("Hello")
    print("Sleeping for 3 seconds")
    time.sleep(3)
    print("Finished sleeping")

def hi():
    print("Hi")
    print("Sleeping for 2 seconds")
    time.sleep(2)
    print("woke up")

#create thread one
t1 = Thread(target=hello)
t2 = Thread(target=hi)

start = time.time()
t1.start()
t2.start()
t1.join()
t2.join()
end = time.time()

print(end -start)

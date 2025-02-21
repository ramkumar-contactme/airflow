import time

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

start = time.time()
hello()
hi()
end = time.time()

print(end -start)

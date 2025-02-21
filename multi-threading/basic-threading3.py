from threading import Thread, current_thread

def repeat(text,count):
    print("Starting the thread :", current_thread().name)
    for i in range(count):
        print(text)

t1=Thread(target=repeat, args=("I love python", 5), name="Repeat Thread")

t1.start()
t1.join()

print("End of the program")

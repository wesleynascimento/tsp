import time
import random
import threading

def rand_num(max_size=1000):

    thread1 = threading.Thread(target=fake_thread)
    thread2 = threading.Thread(target=fake_thread)
    thread3 = threading.Thread(target=fake_thread)
    thread4 = threading.Thread(target=fake_thread)
    thread5 = threading.Thread(target=fake_thread)
    #melhorar fazendo com que as duas threads sejam executadas simultaneamente
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()

    thread5.join()
    thread4.join()
    thread3.join()
    thread2.join()
    thread1.join()

    random.seed(time.time() * random.randint(1, 100000))
    return random.randint(1, max_size)

def fake_thread():
    #make a simple threading
    for x in range(1, random.randint(1,1000)):
        pass
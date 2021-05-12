import threading

def thread_callback():
    print("A")
    print(threading.get_ident())

def thread_callback2():
    print("B")
    print(threading.get_ident())

thr = threading.Thread(target=thread_callback)
thr.start()

thr1 = threading.Thread(target=thread_callback2)
thr1.start()
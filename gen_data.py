import random
import string
import socket
import time
from _thread import *
import threading

def threaded(c):
    while True:
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(16))
        converted = random_string.encode()
        print(converted)
        c.send(converted)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 42180))
    s.listen(5)
    while True:
        c, addr = s.accept()
        print("Connected")
        start_new_thread(threaded, (c,))

if __name__ == '__main__':
    main()
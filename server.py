import socket
import time
from _thread import *
import json
import random
import urllib.request
from Crypto.Cipher import AES

# Adapted from https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Crypto code from https://pypi.org/project/pycrypto/

# TODO
# Pretty much done

def threaded(c):
    key = b'0123456789abcdef'
    iv = b'0123456789abcdef'
    while True:
        '''
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(16))
        converted = random_string.encode()
        '''
        obj = AES.new(key,AES.MODE_CBC, iv=iv) # change key and iv at some point
        url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json")
        words = json.loads(url.read())
        random_word = random.choice(words)
        random_word_bytes = str.encode(random_word)
        random_word_encrypt = obj.encrypt(random_word_bytes*16)
        print(random_word_encrypt)
        time.sleep(0.5)
        c.send(random_word_encrypt)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 42186))
    s.listen(5)
    while True:
        c, addr = s.accept()
        start_new_thread(threaded, (c,))

if __name__ == '__main__':
    main()

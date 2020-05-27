import socket # Standard python library
import time # Standard python library
from _thread import * # Standard python library
import json # Standard python library
import random # Standard python library
import urllib.request # Standard python library
from Crypto.Cipher import AES # https://pypi.org/project/pycryptodome/

def threaded(c): # [8]
    key = b'0123456789abcdef' # define encryption key (must be same as client key)
    iv = b'0123456789abcdef'  # define iv (must be same as client iv)
    while True:
        '''
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(16))
        converted = random_string.encode()
        '''
        obj = AES.new(key,AES.MODE_CBC, iv=iv) # [5] - Initialise encryptor
        url = urllib.request.urlopen("https://raw.githubusercontent.com/sindresorhus/mnemonic-words/master/words.json") # load word list into variable [9]
        words = json.loads(url.read()) # Read word list
        random_word = random.choice(words) # Randomly pick a word
        random_word_bytes = str.encode(random_word) # Encode random word into bytes
        random_word_encrypt = obj.encrypt(random_word_bytes*16) # Pad bytes by 16 and encrypt with previously initialised encyptor
        print(random_word_encrypt) # print encrypted word
        time.sleep(1) # wait 1 second
        c.send(random_word_encrypt) # send to client

# [8]
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Setup server TCP socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Set address reuse
    s.bind(('', 42186)) # Bind localhost to hard coded port
    s.listen(5) # Listen for client connections
    while True: # In a loop
        c, addr = s.accept() # Accept connections
        start_new_thread(threaded, (c,)) # Run above function in a threaded loop

if __name__ == '__main__':
    main()

# [/8]
from zxcvbn import zxcvbn
import random
import requests
import os

# Needs reworking

def main():
    payload = {'username':'sbooth_csc','password':'pass'}
    with requests.Session() as s:
        p = s.post('http://localhost:5000/login', data=payload)
        print (p.text)
        print(s.cookies)


def hold():
    results = zxcvbn(random.choice())
    print(results)
    word = results['password']
    score = results['score']
    print("word:", word)
    print("score:", score)
    if word != 4:
        print("Low string entropy: Its likely traffic is not encrypted")

main()
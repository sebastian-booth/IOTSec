from requests_html import HTMLSession
from bs4 import BeautifulSoup
def main():
    session = HTMLSession()
    render_session = HTMLSession()

    page = session.get('http://localhost:5000/feedback')
    soup = BeautifulSoup(page.content, "lxml")
    print(soup)
    payload = {}
    search = [(element['name']) for element in soup.find_all('input', attrs={'name': True})] # code from https://stackoverflow.com/a/23001729
    print(search)
    for x in search:
        payload.update({x : "<script>document.title = 'XSS Vulnerable' </script>"})
    r = session.post('http://localhost:5000/feedback',payload)
    print("Payload sent")
    render_page = render_session.get('http://localhost:5000/feedback')
    render_page.html.render()
    html = render_page.html.html
    render_soup = BeautifulSoup(html, "lxml")
    title = render_soup.title.string
    print(title)
    if title == "XSS Vulnerable":
        print("The scanned page is vulnerable to XSS")

main()

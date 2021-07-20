# IOTSec - IOT/Web App based security toolkit

Installation instructions  (Linux  -  Ubuntu)\
Enter into terminal:\
cd <extracted code base archive>\
sudo apt install python3  && sudo apt install python3-pip\
pip3 install -r requirements.txt

Operating instructions  (Linux --  Ubuntu)\
IOT environment  must be fully running before any tools.\
Ports 5000 and 3500 must available for web apps and port 42186 must be available for client/server\
socket connection.\
Enter into terminal:\
cd <extracted code base archive>\
python3  server.py\
python3 gui.py\
Prompt -  Input server IP\
python3 hostile.py\
gui.py IOT web frontend can be accessed from http://localhost:5000\
-  /login  --  login user session -  username = csc, password = pass\
-  /protected --  refresh page to display new message from server\
-  /feedback --  enter search query, press filter comments, enter comment, press submit new\
comment\
-  /del-cookies --  deletes all cookies on current page\
-  /logout --  logout current user session\
Hostile.py Hostile web app can be accessed from http://127.0.0.1:3500\
-  (Further instructions given with tools)

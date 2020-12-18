
# ! main loop query format
# Create a chatroom
# 'create';chatroomname;[list of people's UIDs]

# Remove a person from a chatroom
# 'add';chatroomname;toremoveUID

# Add a person to a chatroom
# 'add';chatroomname;newpersonUID

# Add a msg to a chatroom
# todo todo

# ! Server client query format
# Client tells server he is online
# UID;online

# Client tells server he is offline
# UID;ofline

# Client tells server to create a chatroom
# UID;create;targetUID;chatroomname;[; seperated UIDs of members]
# for each targetUID in list of UIDs

# Client tells server to remove themselves from a chatroom
# UID;remove;targetUID;chatroomname
# for each targetUID in list of UIDs

# Client tells server to add a person to a chatroom
# UID;addper;targetUID;chatroomname;newpersonUID
# for each targetUID in people in the chatroom

# Client send a message on a particular chatroom
# UID;send;targetUID;chatroomname;time;msg
# for each targetUID in people in the chatroom

import socket
import selectors
import requests

BUFSIZ = 4096

selfIp = socket.gethostbyname(socket.gethostname())
selfPort = 16384

ip_table = { }
req_table = { }

endpoint = 'https://ipinfo.io/json'
response = requests.get(endpoint, verify = True)
publicip = None
if response.status_code != 200:
    print('Status:', response.status_code, 'Problem with the request. Exiting.')
else:
    data = response.json()
    publicip = data['ip']

#socketManager = selectors.DefaultSelector(  )
listener = socket.socket( family = socket.AF_INET, type = socket.SOCK_STREAM )
listener.bind(("", selfPort))
while True:
    print(publicip)
    print(selfIp)
    listener.listen(1024)
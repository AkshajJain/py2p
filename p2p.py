
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

BUFSIZ = 4096

selfIp = socket.gethostbyname(socket.gethostname())
selfPort = 16384

ip_table = { }
req_table = { }

#socketManager = selectors.DefaultSelector(  )
listener = socket.socket( family = socket.AF_INET, type = socket.SOCK_STREAM )
listener.bind(("", selfPort))
listener.settimeout(0.1)
listener.listen()

whitelisted_ips = ["106.201.123.139", "106.200.238.248", "49.207.201.183", "49.37.170.237", "49.207.201.250", "171.61.90.0", "49.207.223.177"]


listener.setblocking(False)

socketManager = selectors.DefaultSelector()

print('I am', (selfIp, selfPort))


def acc(sock):
    global ip_table, req_table
    conn, addr = sock.accept()
    print("conn:", conn)
    print("addr:", addr)
    conn.setblocking(False)
    socketManager.register(conn, selectors.EVENT_READ, read)

def read(sock):
    global ip_table, req_table
    msg, addr = sock.recvfrom(BUFSIZ)
    print('msg:', msg)
    print('addr:', addr)
    if msg:
        msg = (msg.decode()).split(';')

        sender = msg[0] # This is the UID of the sender
        query = msg[1] # This is the actual query of the user

        # Add phone number to table
        if(query == 'online'):
            ip_table.setdefault(sender, sock)
            print(ip_table)

        # Remove phone number to table
        elif(query == 'ofline'):
            try:
                ip_table.pop(sender)
                sock.close()
                print(ip_table)
            except Exception as e:
                print(ip_table)

        # Create a chatroom with a certain name for a certain user
        elif(query == 'create'):

            target = msg[2]
            name = msg[3]

            UIDs = [sender]
            for UID in msg[4:]: UIDs.append(UID)

            if(req_table.get(target, None) is None):
                req_table[target] = []
            req_table[target].append(['create', name, UIDs])

        # Remove a person from the chatroom of other people
        elif(query == 'remove'):

            target = msg[2]
            name = msg[3]

            if(req_table.get(target, None) is None):
                req_table[target] = []
            req_table[target].append(['remove', name, sender])

        # Send a message to a person on a particular chatroom
        elif(query == 'send'):

            target = msg[2]
            name = msg[3]

            # data = msg[4]

            data = msg[4:]
            temp = ''
            for elem in data: temp += elem + ';'
            data = temp[:-1]

            if(req_table.get(target, None) is None):
                req_table[target] = []
            req_table[target].append(['recv', name, sender, data])

        elif(query == 'addper'):

            target = msg[2]
            name = msg[3]
            toAdd = msg[4]

            if(req_table.get(target, None) is None):
                req_table[target] = []
            req_table[target].append(['addper', name, toAdd])

socketManager.register(listener, selectors.EVENT_READ, acc)

def networking( ):
    global whitelisted_ips
    for ip in whitelisted_ips:
        try:
            listener.connect((ip, selfPort))
        except Exception as e:
            pass
    for key in req_table:
        if(not (ip_table.get(key, None) is None)):
            for query in req_table[key]:
                print(query)
                msg = query[0] + ';' + query[1] + ';'
                if(query[0] == 'create'):
                    for UID in query[2]:
                        msg += UID + ';'
                    msg = msg[:-1:]

                elif(query[0] == 'remove'):
                    msg += query[2]

                elif(query[0] == 'recv'):
                    msg += query[2] + ';' + query[3]

                elif(query[0] == 'addper'):
                    msg += query[2]

                ip_table[key].sendall(msg.encode('utf8'))

            req_table[key] = []

    events = socketManager.select(timeout = 0.01)
    for(key, mask) in events:
        key.data(key.fileobj)


while True: networking( )
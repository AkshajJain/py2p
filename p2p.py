import sys, selectors, socket

logger = sys.stdout

class stdout_():

    def __init__(self, sock):
        self.flag = False
        self.sock = sock

    def write(self, mes):
        self.flag = True
        self.sock.send(mes.encode("UTF8"))

class myClient:

    def __init__(self, socket):
        self.sock = socket
        self.msg = b""

    def sendMsg(self):

        old, sys.stdout = sys.stdout, stdout_(self.sock)
        exec(self.msg.decode(), globals())
        if(not sys.stdout.flag): print('\n', end='')
        self.clearMsg()
        sys.stdout = old

    def clearMsg(self):
        self.msg = b""

    def fileno(self):
        return self.sock.fileno()


def accept(sock):
    conn, addr = sock.accept()
    logger.write('Accepted connection from' + str(addr) + '\n')
    conn.setblocking(False)

    clientConn = myClient(conn)
    socketmanager.register(clientConn, selectors.EVENT_READ, read)

def read(client):
    msg = client.sock.recv(1024)
    client.msg += msg
    logger.write('recieved ' + msg.decode() + ' from ' + str(client.sock.getpeername()) + '\n')

    if(b"\n" in msg):
        if(client.msg == b"q\n"):
            logger.write('Closing ' + str(client.sock.getpeername()) + '\n')
            socketmanager.unregister(client)
            client.sock.close()
        else:
            client.sendMsg()

socketmanager = selectors.DefaultSelector()

s = socket.socket()
s.bind(("", 9999))
s.listen()
s.setblocking(False)

socketmanager.register(s, selectors.EVENT_READ, accept)

while True:
    events = socketmanager.select(timeout=None)
    for(key, mask) in events: key.data(key.fileobj)

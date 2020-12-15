import socket, sys, time
from multiprocessing import Process


def main():
    while True:
        mode = int(input('Choose an action:\n1 | Chat\n2 | Exit\n'))
        if mode == 1:
            chat()
        elif mode == 2:
            sys.exit()
        else:
            print("Not valid.\n")


def chat():
    ip = input("Enter an IP address to connect to: ")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", port))
    print("punching")
    sock.sendto(b'', (ip, port))
    print('Sent 1')
    data, addr = sock.recvfrom(1024)
    print(addr)
    sock.sendto(b'', (ip, port))
    print("punched")
    serverProcess = Process(target=server, args=(ip, sock, port))  # creates server subprocess
    serverProcess.start()
    print("Server process started")
    client(ip, sock, serverProcess)


def server(host, s, p):
    connected = False
    # s.sendto(b"", (host, p))  # attempts connection
    # s.sendto(b"", ("106.201.123.139", p))
    # s.sendto(b"", ("34.197.61.81", p))
    while True:
        data, addr = s.recvfrom(1024)
        print('address:', addr)
        # if not connected:  # no previous data received
        #     print("Connected to %s\n" % host)
        #     s.sendto(b"", (host, p))
        #     connected = True
        if data:
            if data.decode("UTF-8") == "exit":
                print("User disconnected. Type 'exit' to exit.")
            else:
                print(host + ': ' + str(data.decode("UTF-8")))


def client(host, s, serverProcess):
    while True:
        m = str(input())
        enc = m.encode("UTF-8")
        s.sendto(enc, (host, port))  # sends message
        if m == "exit":
            serverProcess.terminate()
            s.close()
            main()


if __name__ == "__main__":
    port = 6311
    main()

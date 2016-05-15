#coding=UTF-8

import sys
import socket
import thread

class Node:
    def __init__(self, nickname, port):
        self.__nickname = nickname
        self.__port = port
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(("0.0.0.0", port))
        self.__server.listen(5)
        thread.start_new_thread(self.listen, ())

    def connect(self, addr):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        client.send("fuck")
        response = client.recv(4096)
        print(response)

    def handle_client(self, client_socket):
        request = client_socket.recv(1024)
        print("received %s" % request)
        client_socket.send("ACK")
        client_socket.close()

    def listen(self):
        while True:
            print("Listening...")
            try:
                client, addr = self.__server.accept()
                print("connection from: %s:%d" % (addr[0], addr[1]))
            except KeyboardInterrupt:
                break
            thread.start_new_thread(self.handle_client, (client,))

def main(argv):
    node = Node("txx", int(argv[1]))
    while True:
        line = sys.stdin.readline()
        ws = line.split()
        if ws[0] == 'connect':
            node.connect((ws[1], int(ws[2])))

if __name__ == '__main__':
    main(sys.argv)
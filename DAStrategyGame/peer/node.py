#coding=UTF-8

import sys, socket, thread, time
import message

UUID = int(round(time.time() * 1000))
MSG = message.Message(UUID)

class Node:
    def __init__(self, nickname, port):
        self.__nickname = nickname
        self.__nodeList = []
        self.__port = port
        self.__uuid = UUID
        self.__msg = MSG
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(('0.0.0.0', port))
        self.__server.listen(5)
        thread.start_new_thread(self.listen, ())

    def send_message(self, addr, msg):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        client.send(msg)
        response = client.recv(4096)
        print(response)
        self.handle_message(client, response)
        client.close()

    def handle_client(self, client_socket):
        request = client_socket.recv(1024*1024)
        print('received %s' % request)
        self.handle_message(client_socket, request)
        client_socket.close()

    def handle_message(self, socket, msg):
        msg = self.__msg.parse(msg)
        if msg['level'] == 'app':
            if msg['type'] == 'requireNodeList':
                socket.send(self.__msg.provideNodeList(self.__nodeList))
            elif msg['type'] == 'provideNodeList':
                print('merge list')

    def listen(self):
        while True:
            print('Listening...')
            try:
                client, addr = self.__server.accept()
                print('connection from: %s:%d' % (addr[0], addr[1]))
            except KeyboardInterrupt:
                break
            thread.start_new_thread(self.handle_client, (client,))

def main(argv):
    node = Node('txx', int(argv[1]))
    while True:
        line = sys.stdin.readline()
        ws = line.split()
        if ws[0] == 'connect':
            node.send_message((ws[1], int(ws[2])), MSG.requireNodeList())

if __name__ == '__main__':
    main(sys.argv)
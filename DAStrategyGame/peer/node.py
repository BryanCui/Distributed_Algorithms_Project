#coding=UTF-8

import sys, socket, thread, time, logging
import message

logging.getLogger().setLevel(logging.INFO)

class Node:
    def __init__(self, nickname, port):
        self.__nickname = nickname
        self.__nodeList = [] # [(nickname:int, ip:str, port:int)]
        self.__port = port
        self.__uuid = int(round(time.time() * 1000))
        self.__msg = message.Message(self.__uuid, port)
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind(('0.0.0.0', port))
        self.__server.listen(5)
        thread.start_new_thread(self.listen, ())

    @property
    def msg(self):
        return self.__msg

    @property
    def nodeList(self):
        return self.__nodeList

    def send_message(self, addr, msg):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        client.send(msg)
        response = client.recv(1024*1024)
        logging.info(response)
        self.handle_message(client, addr, response)
        client.close()

    def handle_client(self, client_socket, addr):
        request = client_socket.recv(1024*1024)
        logging.info('received %s' % request)
        self.handle_message(client_socket, addr, request)
        client_socket.close()

    def handle_message(self, socket, addr, msg):
        msg = self.msg.parse(msg)
        # check if this message is from an unknown node, add it to nodeList
        if not self.hasNode(msg['uuid']):
            node = (msg['uuid'], addr[0], msg['port'])
            self.nodeList.append(node)
            logging.info('add node (%d,%s,%d)' % node)

        if msg['level'] == 'app':
            logging.info('receive msg type: %s' % msg['type'])
            if msg['type'] == 'requireNodeList':
                # reply with local node list
                socket.send(self.msg.provideNodeList(self.nodeList))
                logging.info('send: %s' % self.msg.provideNodeList(self.nodeList))
            elif msg['type'] == 'provideNodeList':
                # update local node list
                logging.info('before updating node list: %s' % self.nodeList)
                for node in msg['list']:
                    if not self.hasNode(node[0]) and node[0] != self.__uuid:
                        self.nodeList.append(node)
                logging.info('updated node list: %s' % self.nodeList)
            else:
                logging.info('do nothing')
        elif msg['level'] == 'snapshot':
            logging.info('todo')
        elif msg['level'] == 'transaction':
            if msg['type'] == 'startTransaction':
                socket.send(self.msg.confirmStartTransaction())
            elif msg['type'] == 'confirmStartTransaction':
                resource = msg['resource']
                quantity = msg['quantity']
                socket.send(self.msg.buyResource(resource, quantity))
            elif msg['type'] == 'buyResource':
                resource = msg['resource']
                quantity = msg['quantity']
                socket.send(self.msg.sellResource(resource, quantity))
            elif msg['type'] == 'finishTransaction':
                socket.send(self.msg.finishTransaction())
            elif msg['type'] == 'confirmFinishTransaction':
                socket.send(self.msg.confirmFinishTransaction())

    def hasNode(self, uuid):
        for node in self.nodeList:
            if node[0] == uuid:
                return True
        return False


    def listen(self):
        while True:
            logging.info('Listening...')
            try:
                client, addr = self.__server.accept()
                logging.info('connection from: %s:%d' % (addr[0], addr[1]))
            except KeyboardInterrupt:
                break
            thread.start_new_thread(self.handle_client, (client,addr,))

def main(argv):
    node = Node(argv[1], int(argv[2]))
    while True:
        line = sys.stdin.readline()
        ws = line.split()
        if ws[0] == 'connect':
            node.send_message((ws[1], int(ws[2])), node.msg.requireNodeList())
        elif ws[0] == 'nodelist':
            logging.info('current local node list: %s' % node.nodeList)

if __name__ == '__main__':
    main(sys.argv)
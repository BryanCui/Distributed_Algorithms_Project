# coding=UTF-8

import socket, thread, time, logging
import message
import sys
sys.path.append("../")

from User.User import User
from Transactions import Transactions

logging.getLogger().setLevel(logging.INFO)

router = {
    ('app', 'requireNodeList'): 'onRequireNodeList',
    ('app', 'provideNodeList'): 'onProvideNodeList',
    ('app', 'logout'): 'onLogout',
    ('app', 'ack'): 'onAck',
    ('app', 'startTransaction'): 'onStartTransaction',
    ('app', 'confirmStartTransaction'): 'onConfirmStartTransaction',
    ('app', 'buyResource'): 'onBuyResource',
    ('app', 'sellResource'): 'onSellResource',
    ('app', 'finishTransaction'): 'onFinishTransaction',
    ('app', 'confirmFinishTransaction'): 'onConfirmFinishTransaction',
    ('app', 'showTradingCenter'): 'onShowTradingCenter',
    ('app', 'returnTradingCenter'): 'onReturnTradingCenter',
    ('snapshot', ''): ''
}


class Node(object):
    def __init__(self, nickname, port):
        self._nickname = nickname
        self._nodeList = []  # [(nickname:int, ip:str, port:int)]
        self._port = port
        self._uuid = int(round(time.time() * 1000))
        self._msg = message.Message(self._uuid, port)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(('0.0.0.0', port))
        self._server.listen(5)
        self._user = User()
        print self._user.show_resources()
        thread.start_new_thread(self.listen, ())

    @property
    def msg(self):
        return self._msg

    @property
    def nodeList(self):
        return self._nodeList

    @property
    def user(self):
        return self._user

    def listen(self):
        while True:
            logging.info('Listening...')
            try:
                client, addr = self._server.accept()
                logging.info('connection from: %s:%d' % (addr[0], addr[1]))
            except KeyboardInterrupt:
                break
            thread.start_new_thread(self.handle_client, (client, addr,))

    def send_message(self, addr, msg):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
        client.send(msg)
        response = client.recv(1024 * 1024)
        logging.info(response)
        self.handle_message(client, addr, response)
        client.close()

    def handle_client(self, client_socket, addr):
        request = client_socket.recv(1024 * 1024)
        logging.info('received %s' % request)
        self.handle_message(client_socket, addr, request)
        client_socket.close()

    def handle_message(self, socket, addr, msg):
        msg = self.msg.parse(msg)
        node = (msg['uuid'], addr[0], msg['port'])
        msg_level = msg['level']
        msg_type = msg['type']

        logging.info('receive msg: %s' % msg)

        # check if this message is from an unknown node, add it to nodeList
        if not self.hasNode(msg['uuid']):
            self.nodeList.append(node)
            logging.info('add node (%d,%s,%d)' % node)

        if (msg_level, msg_type) in router:
            cls = self.__class__
            func = cls.__dict__[router[(msg_level, msg_type)]]
            apply(func, (self, socket, addr, node, msg))

    # begin handlers
    def onRequireNodeList(self, socket, addr, node, msg):
        # reply with local node list
        socket.send(self.msg.provideNodeList(self.nodeList))
        logging.info('send: %s' % self.msg.provideNodeList(self.nodeList))

    def onProvideNodeList(self, socket, addr, node, msg):
        # update local node list
        logging.info('before updating node list: %s' % self.nodeList)
        for node in msg['list']:
            if not self.hasNode(node[0]) and node[0] != self._uuid:
                self.nodeList.append(node)
        logging.info('updated node list: %s' % self.nodeList)

    def onLogout(self, socket, addr, node, msg):
        # delete node
        self.deleteNode(msg['uuid'])
        socket.send(self.msg.ack())
        logging.info('deleted node (%d,%s,%d)' % node)

    def onAck(self, socket, addr, node, msg):
        # do nothing yet
        pass

    def onStartTransaction(self, socket, addr, node, msg):
        socket.send(self.msg.confirmStartTransaction())

    def onConfirmStartTransaction(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = msg['quantity']
        socket.send(self.msg.buyResource(resource, quantity))

    def onBuyResource(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = msg['quantity']
        self.get_user().get_trading_center().consume_resources(resource, int(quantity))
        self.get_user().add_money(self.get_user().get_trading_center().earn_money(resource,int(quantity)))
        socket.send(self.msg.sellResource(resource, quantity, self.get_user().get_trading_center().get_resources_price(resource)))

    def onSellResource(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = msg['quantity']
        price = msg['price']
        self.get_user().add_resources(resource, int(quantity))
        self.get_user().consume_money(int(price) * int(quantity))
        socket.send(self.msg.finishTransaction())

    def onFinishTransaction(self, socket, addr, node, msg):
        socket.send(self.msg.confirmFinishTransaction())

    def onConfirmFinishTransaction(self, socket, addr, node, msg):
        return

    def onShowTradingCenter(self, socket, addr, node, msg):
        socket.send(self.msg.returnTradingCenter(self.get_user().get_trading_center().get_trading_list()))

    def onReturnTradingCenter(self, socket, addr, node, msg):
        logging.info(msg['tradingList'])
    # end of handlers


    # begin helpers
    def deleteNode(self, uuid):
        for node in self.nodeList:
            if node[0] == uuid:
                self.nodeList.remove(node)
                break

    def hasNode(self, uuid):
        for node in self.nodeList:
            if node[0] == uuid:
                return True
        return False
    # end of helpers

def main(argv):
    node = Node(argv[1], int(argv[2]))
    # for debug only
    while True:
        line = sys.stdin.readline()
        ws = line.split()
        if ws[0] == 'connect':
            node.send_message((ws[1], int(ws[2])), node.msg.requireNodeList())

        elif ws[0] == 'nodelist':
            logging.info('current local node list: %s' % node.nodeList)
        elif ws[0] == 'logout':
            for n in node.nodeList:
                node.send_message((n[1], n[2]), node.msg.logout())
            logging.info('logged out. bye.')
        elif ws[0] == 'show_resources':
            logging.info(node.user.show_resources())
        elif ws[0] == 'show_trading_center':
            logging.info(node.user.get_trading_center().show_trading_center())
        elif ws[0] == 'put_resource_to_sell':
            node.user.put_resource_into_trading_center(ws[1], int(ws[2]), int(ws[3]))
        elif ws[0] == 'get_resource_back_from_trading_center':
            node.user.get_resource_from_trading_center_back(int(ws[1]), int(ws[2]))
        elif ws[0] == 'get_trading_list':
            node.send_message((ws[1], int(ws[2])), node.msg.showTradingCenter())
        elif ws[0] == 'buy':
            transaction = Transactions(ws[1], node._msg, node, node.user)
            transaction.start_transaction(ws[2], ws[3])


if __name__ == '__main__':
    main(sys.argv)

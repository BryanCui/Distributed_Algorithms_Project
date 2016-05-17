# coding=UTF-8

import socket, thread, time, logging
import message
import sys
sys.path.append("../")

from User.User import User
from Transactions.Transactions import Transactions

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
    def __init__(self, nickname, role, port):
        self._nickname = nickname
        self._nodeList = []  # [(uuid:int, ip:str, port:int, nickname:str)]
        self._port = port
        self._uuid = int(round(time.time() * 1000))
        self._msg = message.Message(self._uuid, port, nickname)
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
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(addr)
            client.send(msg)
            response = client.recv(1024 * 1024)
            logging.info(response)
            msg = self.msg.parse(response)
            self.handle_message(client, addr, msg)
            client.close()
            return msg
        except:
            return False

    def handle_client(self, client_socket, addr):
        request = client_socket.recv(1024 * 1024)
        logging.info('received %s' % request)
        msg = self.msg.parse(request)
        self.handle_message(client_socket, addr, msg)
        client_socket.close()

    def handle_message(self, socket, addr, msg):
        node = (msg['uuid'], addr[0], msg['port'], msg['nickname'])
        msg_level = msg['level']
        msg_type = msg['type']

        logging.info('receive msg: %s' % msg)

        # check if this message is from an unknown node, add it to nodeList
        if not self.hasNode(msg['uuid']) and self._uuid != msg['uuid']:
            self.nodeList.append(node)
            logging.info('add node (%d,%s,%d,%s)' % node)

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
        logging.info('deleted node (%d,%s,%d,%s)' % node)

    def onAck(self, socket, addr, node, msg):
        # do nothing yet
        pass

    def onStartTransaction(self, socket, addr, node, msg):
        socket.send(self.msg.confirmStartTransaction(msg['resource'], int(msg['quantity'])))

    def onConfirmStartTransaction(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = int(msg['quantity'])
        self.send_message(addr, self.msg.buyResource(resource, quantity))

    def onBuyResource(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = int(msg['quantity'])

        self.user.get_trading_center().consume_resources(resource, quantity)
        self.user.add_money(self.user.get_trading_center().earn_money(resource,quantity))
        socket.send(self.msg.sellResource(resource, quantity, self.user.get_trading_center().get_resources_price(resource)))

    def onSellResource(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = int(msg['quantity'])
        price = msg['price']
        self.user.add_resources(resource, quantity)
        self.user.consume_money(int(price) * quantity)
        self.send_message(addr, self.msg.finishTransaction())

    def onFinishTransaction(self, socket, addr, node, msg):
        socket.send(self.msg.confirmFinishTransaction())

    def onConfirmFinishTransaction(self, socket, addr, node, msg):
        return

    def onShowTradingCenter(self, socket, addr, node, msg):
        socket.send(self.msg.returnTradingCenter(self.user.get_trading_center().get_trading_list()))

    def onReturnTradingCenter(self, socket, addr, node, msg):
        for (item, value) in msg['tradingList'].items():
            logging.info(item + ': ' + str(value[0]) + ', Price: ' + str(value[1]))
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
    node = Node(argv[1], 'role', int(argv[2]))
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
        elif ws[0] == 'resource':
            logging.info(node.user.show_resources())
        elif ws[0] == 'trading_center':
            logging.info(node.user.get_trading_center().show_trading_center())
        elif ws[0] == 'sell':
            node.user.put_resource_into_trading_center(ws[1], int(ws[2]), int(ws[3]))
        elif ws[0] == 'get_resource_back_from_trading_center':
            node.user.get_resource_from_trading_center_back(ws[1], int(ws[2]))
        elif ws[0] == 'get_trading_list':
            node.send_message((ws[1], int(ws[2])), node.msg.showTradingCenter())
        elif ws[0] == 'buy':
            transaction = Transactions((ws[1], int(ws[2])), node._msg, node, node.user)
            transaction.start_transaction(ws[3], ws[4])


if __name__ == '__main__':
    main(sys.argv)

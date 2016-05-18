# coding=UTF-8

import socket, thread, time, logging
import message, snapshot
import sys
from notificationCentre import NotificationCentre
sys.path.append("../")

from User.User import User
from Transactions.Transactions import Transactions

logging.getLogger().setLevel(logging.ERROR)

router = {
    ('app', 'notifyNewNode'): 'onNotifyNewNode',
    ('app', 'notifyDeleteNode'): 'onNotifyDeleteNode',
    ('app', 'notifyReplaceNode'): 'onNotifyReplaceNode',
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
    ('app', 'doneTransaction'): 'onDoneTransaction',
    ('app', 'showTradingCenter'): 'onShowTradingCenter',
    ('app', 'returnTradingCenter'): 'onReturnTradingCenter',
    ('app', 'returnActivate'): 'onReturnActivate',
    ('app', 'checkAlive'): 'onCheckAlive',
    ('app', 'alive'): 'onAlive',
    ('snapshot', 'marker'): 'onMarker',
    'app': 'onApp',
}


class Node(object):
    def __init__(self, nickname, port, role):
        self._nickname = nickname
        self._nodeList = []  # [[uuid:int, ip:str, port:int, nickname:str, role:str]]
        self._port = port
        self._uuid = int(round(time.time() * 1000))
        self._msg = message.Message(self._uuid, port, nickname, role)
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(('0.0.0.0', port))
        self._server.listen(5)
        self._user = User(role)
        self._transaction = Transactions('', self._msg, self, self._user)
        self._lastLocalSnapshot = None
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

    @property
    def lastLocalSnapshot(self):
        return self._lastLocalSnapshot
    
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
            logging.info('sending (%s:%d) msg: %s' % (addr[0], addr[1], msg))
            response = client.recv(1024 * 1024)
            logging.info('received %s' % response)
            msg = self.msg.parse(response)
            self.handle_message(client, addr, msg)
            client.close()
            return msg
        except:
            return False

    def oneway_message(self, addr, msg):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(addr)
            client.send(msg)
            logging.info('sending (%s:%d) msg: %s' % (addr[0], addr[1], msg))
            return True
        except:
            return False

    def handle_client(self, client_socket, addr):
        request = client_socket.recv(1024 * 1024)
        logging.info('received %s' % request)
        msg = self.msg.parse(request)
        self.handle_message(client_socket, addr, msg)
        client_socket.close()

    def handle_message(self, socket, addr, msg):
        node = [msg['uuid'], addr[0], msg['port'], msg['nickname'], msg['role']]
        addr = (addr[0], msg['port'])
        msg_level = msg['level']
        msg_type = msg['type']

        # check if this message is from an unknown node, add it to nodeList
        if not self.hasNode(msg['uuid']) and self._uuid != msg['uuid']:
            # if (ip, port) duplicates, then replace
            preNode = self.getNode(node[1], node[2])
            if preNode != None:
                self.nodeList.remove(preNode)
                self.nodeList.append(node)
                for n in self.nodeList:
                    self.oneway_message((n[1], n[2]), self.msg.notifyReplaceNode(preNode, node))
                logging.info('replace node %s with node %s' % (preNode, node))
            else:
                self.nodeList.append(node)
                # notify the other node in my list
                for n in self.nodeList:
                    self.oneway_message((n[1], n[2]), self.msg.notifyNewNode(node))
                logging.info('add node %s' % node)

        if msg_level in router:
            cls = self.__class__
            func = cls.__dict__.get(router[msg_level], None)
            if func == None:
                cls = cls.__bases__[0]
                func = cls.__dict__[router[msg_level]]
                apply(func, (self, socket, addr, node, msg))
            else:
                apply(func, (self, socket, addr, node, msg))

        if (msg_level, msg_type) in router:
            cls = self.__class__
            func = cls.__dict__.get(router[(msg_level, msg_type)], None)
            if func == None:
                cls = cls.__bases__[0]
                func = cls.__dict__[router[(msg_level, msg_type)]]
                apply(func, (self, socket, addr, node, msg))
            else:
                apply(func, (self, socket, addr, node, msg))

    # begin handlers
    def onNotifyReplaceNode(self, socket, addr, node, msg):
        preNode = [msg['preNode']['uuid'], msg['preNode']['ip'], msg['preNode']['port'], msg['preNode']['nickname'], msg['preNode']['role']]
        postNode = [msg['postNode']['uuid'], msg['postNode']['ip'], msg['postNode']['port'], msg['postNode']['nickname'], msg['postNode']['role']]
        if preNode in self.nodeList:
            self.nodeList.remove(preNode)
        if postNode not in self.nodeList:
            self.nodeList.append(postNode)
        logging.info('replace node %s with node %s' % (preNode, postNode))

    def onNotifyDeleteNode(self, socket, addr, node, msg):
        node = [msg['node']['uuid'], msg['node']['ip'], msg['node']['port'], msg['node']['nickname'], msg['node']['role']]
        if node in self.nodeList:
            self.nodeList.remove(node)
            logging.info('delete node %s' % node)

    def onNotifyNewNode(self, socket, addr, node, msg):
        node = [msg['node']['uuid'], msg['node']['ip'], msg['node']['port'], msg['node']['nickname'], msg['node']['role']]
        if node not in self.nodeList and node[0] != self._uuid:
            self.nodeList.append(node)
            logging.info('add node %s' % node)

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
        logging.info('deleted node %s' % node)

    def onAck(self, socket, addr, node, msg):
        # do nothing yet
        pass

    def onCheckAlive(self, socket, addr, node, msg):
        socket.send(self.msg.alive())

    def onAlive(self, socket, addr, node, msg):
        pass

    def onStartTransaction(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = int(msg['quantity'])
        self._transaction.confirm_start_transaction(socket, resource, quantity)


    def onConfirmStartTransaction(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = int(msg['quantity'])
        self._transaction.buy_resource(addr, resource, quantity)

    def onBuyResource(self, socket, addr, node, msg):
        resource = msg['resource']
        quantity = int(msg['quantity'])
        price = self.user.trading_center.get_resources_price(resource)
        self._transaction.sell_resource(socket, resource, quantity, price)

    def onSellResource(self, socket, addr, node, msg):
        self._transaction.finish_transaction(addr, msg)

    # Handle the Return of Activate Info
    def onReturnActivate(self, socket, addr, node, msg):
        balance = int(msg['balance'])
        if balance > 0:
            self.user.add_money(balance)
            self.user.show_resources()
            self.fire_notification()
        logging.info("%s, withdraw %s "%(msg['info'],msg['balance']))


    def onFinishTransaction(self, socket, addr, node, msg):
        self._transaction.confirm_finish_transaction(socket)

    def onConfirmFinishTransaction(self, socket, addr, node, msg):
        self._transaction.done_transaction(addr)
        self._transaction.set_finished(True)
        NotificationCentre.defaultCentre().fire('transaction_finish', 'True')
        self.fire_notification()

    def onDoneTransaction(self, socket, addr, node, msg):
        self._transaction.set_finished(True)
        NotificationCentre.defaultCentre().fire('transaction_finish', 'True')
        self.fire_notification()

    def onShowTradingCenter(self, socket, addr, node, msg):
        socket.send(self.msg.returnTradingCenter(self.user.trading_center.get_trading_list()))

    def onReturnTradingCenter(self, socket, addr, node, msg):
        for (item, value) in msg['tradingList'].items():
            logging.info(item + ': ' + str(value[0]) + ', Price: ' + str(value[1]))

    def onMarker(self, socket, addr, node, msg):
        if self.lastLocalSnapshot == None or self.lastLocalSnapshot.isDone == True:
            # take new snapshot
            self._lastLocalSnapshot = snapshot.NodeSnapshot(nodeList=self.nodeList)
            self.lastLocalSnapshot.recordLocalState(self)
            self.lastLocalSnapshot.finishRecord(node)
            # send marker to all known node
            for n in self.nodeList:
                self.oneway_message((n[1], n[2]), self.msg.snapshotMarker())
        else:
            # continue current snapshot
            self.lastLocalSnapshot.finishRecord(node)
        # check if snapshot is done
        if self.lastLocalSnapshot.isDone == True:
            pass

    def onApp(self, socket, addr, node, msg):
        if self.lastLocalSnapshot != None and self.lastLocalSnapshot.isDone == False:
            if self.lastLocalSnapshot.isRecording(node):
                self.lastLocalSnapshot.recordMessage(node, msg)

    def localState(self):
        off = self.user.get_user_resource_status()
        on = self.user.get_trading_center_status()
        result = {k:{'for trade': on.get(k, (0,0))[0], 'price': on.get(k, (0,0))[1], 'stock': off[k]} for k in off.keys()}
        return result

    # end of handlers

    def startSnapshot(self):
        if self.lastLocalSnapshot != None and self.lastLocalSnapshot.isDone == False:
            return False
        else:
            self._lastLocalSnapshot = snapshot.NodeSnapshot(nodeList=self.nodeList)
            for n in self.nodeList:
                self.oneway_message((n[1], n[2]), self.msg.snapshotMarker())
            return True

    def logout(self):
        for n in self.nodeList:
            self.send_message((n[1], n[2]), self.msg.logout())
        logging.info('logged out. bye.')
        return True

    def checkAlive(self):
        for n in self.nodeList:
            result = self.send_message((n[1], n[2]), self.msg.checkAlive())
            if result == False:
                self.nodeList.remove(n)
                for nn in self.nodeList:
                    self.oneway_message((nn[1], nn[2]), self.msg.notifyDeleteNode(n))
                logging.info('deleted node %s' % n)
        return True

    def activate(self, addr, cdkey):
        return self.send_message(addr, node.msg.activateCdkey(cdkey))

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

    def getNode(self, ip, port):
        for node in self.nodeList:
            if node[1] == ip and node[2] == int(port):
                return node
        return None
    # end of helpers

    def start_transaction(self, addr, resource, quantity):
        self._transaction = Transactions(addr, self._msg, self, self.user)
        self._transaction.start_transaction(resource, quantity)

    def fire_notification(self):
        NotificationCentre.defaultCentre().fire('resource_change', {
            'food': self.user.get_food(),
            'wood': self.user.get_wood(),
            'mineral': self.user.get_mineral(),
            'leather': self.user.get_leather(),
            'money': self.user.get_money()
        })

        NotificationCentre.defaultCentre().fire('trading_change', {
            'food': (self.user.trading_center.get_food(), self.user.trading_center.get_food_price()),
            'wood': (self.user.trading_center.get_wood(), self.user.trading_center.get_wood_price()),
            'mineral': (self.user.trading_center.get_mineral(), self.user.trading_center.get_mineral_price()),
            'leather': (self.user.trading_center.get_leather(), self.user.trading_center.get_leather_price())
        })

def main(argv):
    node = Node(argv[1], int(argv[2]), argv[3])
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
        elif ws[0] == 'show':
            logging.info(node.send_message((ws[1], int(ws[2])), node.msg.showTradingCenter()))
        elif ws[0] == 'resource':
            logging.info(node.user.show_resources())
        elif ws[0] == 'trading_center':
            logging.info(node.user.trading_center.show_trading_center())
        elif ws[0] == 'sell':
            node.user.put_resource_into_trading_center(ws[1], int(ws[2]), int(ws[3]))
        # activate cdkey argv[3]: ip, port, cdkey
        elif ws[0] == "activate" and len(ws) == 4:
            node.send_message((ws[1], int(ws[2])), node.msg.activateCdkey(ws[3]))

        elif ws[0] == 'get_resource_back_from_trading_center':
            node.user.get_resource_from_trading_center_back(ws[1], int(ws[2]))
        elif ws[0] == 'get_trading_list':
            node.send_message((ws[1], int(ws[2])), node.msg.showTradingCenter())
        elif ws[0] == 'buy':
            node._transaction = Transactions((ws[1], int(ws[2])), node._msg, node, node.user)
            node._transaction.start_transaction(ws[3], ws[4])
        # elif ws[0] == 'snapshot':



if __name__ == '__main__':
        main(sys.argv)

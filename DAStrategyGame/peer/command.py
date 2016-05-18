# coding=UTF-8

import sys, logging
from notificationCentre import NotificationCentre
from node import Node
# logging.getLogger().setLevel(logging.INFO)

route = {
    'createGame': 'createGame',
    'joinGame': 'joinGame',
    'connect': 'inquireNodeList',
    'nodeList': 'localNodeList',
    'show': 'localResource',
    'remote': 'remoteNodeResource',
    'tradingCenter': 'tradingCenter',
    'snapshot': 'startSnapshot',
    'checkAlive': 'checkAlive',
    'trade': 'toTrade',
    'stock': 'toStock',
    'buy': 'buy',
    'activate': 'activate',
    'logout': 'logout'
}

class Command(object):

    def __init__(self):
        self._node = None

    @property
    def node(self):
        return self._node

    def execute(self, cmd, *args):
        if cmd not in route:
            return False
        fName = route[cmd]
        if fName in ['createGame', 'joinGame']:
            if self.node != None:
                return False
        else:
            if self.node == None:
                return False
        cls = self.__class__
        func = cls.__dict__[fName]
        return apply(func, (self,)+args)

    # begin commands
    def createGame(self, nickname, role, port):
        node = Node(nickname, int(port), role)
        self._node = node
        return True

    def joinGame(self, nickname, role, port, addr):
        node = Node(nickname, int(port), role)
        self._node = node
        response = node.send_message(addr, node.msg.requireNodeList())
        if response == False:
            return False
        return True

    def inquireNodeList(self, addr):
        response = self.node.send_message(addr, self.node.msg.requireNodeList())
        return False

    def localNodeList(self):
        return self.node.nodeList

    def localResource(self):
        return self.node.localState()    

    def tradingCenter(self):
        return self.node.user.get_trading_center_status()

    def remoteNodeResource(self, addr):
        response = self.node.send_message(addr, self.node.msg.showTradingCenter())
        return response['tradingList']

    def startSnapshot(self):
        return self.node.startSnapshot()

    def checkAlive(self):
        return self.node.checkAlive()

    def logout(self):
        result = self.node.logout()
        sys.exit(0)
        return result

    def toTrade(self, resource, num, price):
        return self.node.user.put_resource_into_trading_center(resource, int(num), int(price))

    def toStock(self, resource, num):
        return self.node.user.get_resource_from_trading_center_back(resource, int(num))

    def buy(self, addr, resource, num):
        return self.node.start_transaction(addr, resource, int(num))

    def activate(self, addr, cdkey):
        return self.node.send_message(addr, self.node.msg.activateCdkey(cdkey))

    # login nickname role address(ip:port)
    # 

    # end of commands

def main(argv):
    command = Command()
    if len(argv) == 4:
        command.execute('createGame', argv[1], argv[2], int(argv[3]))
    elif len(argv) == 6:
        command.execute('joinGame', argv[1], argv[2], int(argv[3]), (argv[4], int(argv[5])))
    else:
        return

    while True:
        line = sys.stdin.readline()
        if len(line) < 2:
            continue
        ws = line.split()
        result = None
        logging.info(ws[0])
        if ws[0] == 'connect':
            result = command.execute('connect', (ws[1], int(ws[2])))
        elif ws[0] == 'nodelist':
            result = command.execute('nodeList')
        elif ws[0] == 'logout':
            result = command.execute('logout')
        elif ws[0] == 'show':
            result = command.execute('show')
        elif ws[0] == 'buy':
            result = command.execute('buy', (ws[1], int(ws[2])), ws[3], int(ws[4]))
        elif ws[0] == 'stock':
            result = command.execute('stock', ws[1], int(ws[2]))
        elif ws[0] == 'trade':
            result = command.execute('trade', ws[1], int(ws[2]), int(ws[3]))
        elif ws[0] == 'remote':
            result = command.execute('remote', (ws[1], int(ws[2])))
        elif ws[0] == 'activate':
            result = command.execute('activate', (ws[1], int(ws[2])), ws[3])
        elif ws[0] == 'tradingCenter':
            result = command.execute('tradingCenter')
        # elif ws[0] == 'resource':
        #     logging.info(node.user.show_resources())
        # elif ws[0] == 'trading_center':
        #     logging.info(node.user.get_trading_center().show_trading_center())
        # elif ws[0] == 'sell':
        #     node.user.put_resource_into_trading_center(ws[1], int(ws[2]), int(ws[3]))
        # elif ws[0] == 'get_resource_back_from_trading_center':
        #     node.user.get_resource_from_trading_center_back(ws[1], int(ws[2]))
        # elif ws[0] == 'get_trading_list':
        #     node.send_message((ws[1], int(ws[2])), node.msg.showTradingCenter())
        # elif ws[0] == 'buy':
        #     node._transaction = Transactions((ws[1], int(ws[2])), node._msg, node, node.user)
        #     node._transaction.start_transaction(ws[3], ws[4])
        elif ws[0] == 'snapshot':
            result = command.execute('snapshot')
        elif ws[0] == 'checkAlive':
            result = command.execute('checkAlive')
        elif ws[0] == 'localResource':
            result = command.execute('localResource')
        elif ws[0] == 'exit':
            sys.exit(0)
        
        logging.info(result)



if __name__ == '__main__':
    # [command.py txx role port]
    # [command.py txx role port remoteIP remotePort]
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        sys.exit(0)

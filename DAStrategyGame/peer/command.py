# coding=UTF-8

from node import Node

route = {
    'createGame': 'createGame',
    'joinGame': 'joinGame',
    'inquireNodeList': 'inquireNodeList',
    'localNodeList': 'localNodeList',
    'localResource': 'localResource',
    'remoteNodeResource': 'remoteNodeResource', # lao cui!
}

class Command(object):

    def __init__(self):
        self._node = None

    @property
    def node(self):
        return self._node
    

    def excute(self, cmd, *args=()):
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
        node = Node(nickname, role, port)
        self.node = node
        return True

    def joinGame(self, nickname, role, addr):
        node = Node(nickname, role, port)
        self.node = node
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
        return self.node.user.resources()    

    def remoteNodeResource(self, addr):
        response = self.node.send_message(addr, self.node.msg.showTradingCenter())
        return response['tradingList']


    # login nickname role address(ip:port)
    # 

    # end of commands
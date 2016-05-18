import json
import sys

class Message:

    def __init__(self, uuid, port, nickname, role):
        self.__uuid = uuid
        self.__port = port
        self.__nickname = nickname
        self.__role = role

    def basic(self):
        return {'uuid': self.__uuid, 'port': self.__port, 'nickname': self.__nickname, 'role':self.__role}

    def checkAlive(self):
        msg = {'level': 'app', 'type': 'checkAlive'}
        msg.update(self.basic())
        return json.dumps(msg)

    def alive(self):
        msg = {'level': 'app', 'type': 'alive'}
        msg.update(self.basic())
        return json.dumps(msg)

    def notifyReplaceNode(self, preNode, postNode):
        msg = {'level': 'app', 'type': 'notifyReplaceNode', 'preNode': {'uuid': preNode[0], 'ip': preNode[1], 'port': preNode[2], 'nickname': preNode[3], 'role': preNode[4]}, 
            'postNode': {'uuid': postNode[0], 'ip': postNode[1], 'port': postNode[2], 'nickname': postNode[3], 'role': postNode[4]}}
        msg.update(self.basic())
        return json.dumps(msg)

    def notifyDeleteNode(self, node):
        msg = {'level': 'app', 'type': 'notifyDeleteNode', 'node': {'uuid': node[0], 'ip': node[1], 'port': node[2], 'nickname': node[3], 'role': node[4]}}
        msg.update(self.basic())
        return json.dumps(msg)

    def notifyNewNode(self, node):
        msg = {'level': 'app', 'type': 'notifyNewNode', 'node': {'uuid': node[0], 'ip': node[1], 'port': node[2], 'nickname': node[3], 'role': node[4]}}
        msg.update(self.basic())
        return json.dumps(msg)

    def requireNodeList(self):
        msg = {'level': 'app', 'type': 'requireNodeList'}
        msg.update(self.basic())
        return json.dumps(msg)

    def provideNodeList(self, list):
        msg = {'level': 'app', 'type': 'provideNodeList', 'list': list}
        msg.update(self.basic())
        return json.dumps(msg)

    def logout(self):
        msg = {'level': 'app', 'type': 'logout'}
        msg.update(self.basic())
        return json.dumps(msg)

    def ack(self):
        msg = {'level': 'app', 'type': 'ack'}
        msg.update(self.basic())
        return json.dumps(msg)

    def answerActivate(self, info='success', balance='0'):
        msg = {'level': 'app', 'type': 'returnActivate','info': info , 'balance': balance}
        msg.update(self.basic())
        return json.dumps(msg)

    def activateCdkey(self, cdkey):
        msg = {'level': 'app', 'type': 'activate', 'cdkey': cdkey}
        msg.update(self.basic())
        return json.dumps(msg)

    def startTransaction(self, resource, quantity):
        msg = {'level': 'app', 'type': 'startTransaction', 'resource':resource, 'quantity': quantity}
        msg.update(self.basic())
        return json.dumps(msg)

    def confirmStartTransaction(self, resource, quantity):
        msg = {'level': 'app', 'type': 'confirmStartTransaction', 'resource':resource, 'quantity': quantity}
        msg.update(self.basic())
        return json.dumps(msg)

    def finishTransaction(self):
        msg = {'level': 'app', 'type': 'finishTransaction'}
        msg.update(self.basic())
        return json.dumps(msg)

    def confirmFinishTransaction(self):
        msg = {'level': 'app', 'type': 'confirmFinishTransaction'}
        msg.update(self.basic())
        return json.dumps(msg)

    def doneTransaction(self):
        msg = {'level': 'app', 'type': 'doneTransaction'}
        msg.update(self.basic())
        return json.dumps(msg)

    def buyResource(self, resource, quantity):
        msg = {'level': 'app', 'type': 'buyResource', 'resource':resource, 'quantity': quantity}
        msg.update(self.basic())
        return json.dumps(msg)

    def sellResource(self, resource, quantity, price):
        msg = {'level': 'app', 'type': 'sellResource', 'resource':resource, 'quantity': quantity, 'price': price}
        msg.update(self.basic())
        return json.dumps(msg)

    def showTradingCenter(self):
        msg = {'level': 'app', 'type': 'showTradingCenter'}
        msg.update(self.basic())
        return json.dumps(msg)

    def returnTradingCenter(self, list):
        msg = {'level': 'app', 'type': 'returnTradingCenter', 'tradingList': list}
        msg.update(self.basic())
        return json.dumps(msg)

    def transactionRunning(self):
        msg = {'level': 'app', 'type': 'transactionRunning'}
        msg.update(self.basic())
        return json.dumps(msg)

    def snapshotMarker(self):
        msg = {'level': 'snapshot', 'type': 'marker'}
        msg.update(self.basic())
        return json.dumps(msg)

    def parse(self, msg):
        return json.loads(msg)

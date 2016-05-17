import json
import sys

class Message:

    def __init__(self, uuid, port, nickname):
        self.__uuid = uuid
        self.__port = port
        self.__nickname = nickname

    def basic(self):
        return {'uuid': self.__uuid, 'port': self.__port, 'nickname': self.__nickname}

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
        msg = {'level': 'app', 'type': 'answerActivate','info': info , 'balance': balance}
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

    def parse(self, msg):
        return json.loads(msg)

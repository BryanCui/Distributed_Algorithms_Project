import json
import sys

class Message:

    def __init__(self, uuid, port):
        self.__uuid = uuid
        self.__port = port

    def requireNodeList(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'requireNodeList'}
        return json.dumps(msg)

    def provideNodeList(self, list):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'provideNodeList', 'list': list}
        return json.dumps(msg)

    def logout(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'logout'}
        return json.dumps(msg)

    def ack(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'ack'}
        return json.dumps(msg)

    def activateCdkey(self, cdkey):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'activate', 'cdkey': cdkey}
        return json.dumps(msg)

    def startTransaction(self, resource, quantity):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'startTransaction', 'resource':resource, 'quantity': quantity}
        return json.dumps(msg)

    def confirmStartTransaction(self, resource, quantity):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'confirmStartTransaction', 'resource':resource, 'quantity': quantity}
        return json.dumps(msg)

    def finishTransaction(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'finishTransaction'}
        return json.dumps(msg)

    def confirmFinishTransaction(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'confirmFinishTransaction'}
        return json.dumps(msg)

    def buyResource(self, resource, quantity):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'buyResource', 'resource':resource, 'quantity': quantity}
        return json.dumps(msg)

    def sellResource(self, resource, quantity, price):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'sellResource', 'resource':resource, 'quantity': quantity, 'price': price}
        return json.dumps(msg)

    def showTradingCenter(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'showTradingCenter'}
        return json.dumps(msg)

    def returnTradingCenter(self, list):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'app', 'type': 'returnTradingCenter', 'tradingList': list}
        return json.dumps(msg)

    def parse(self, msg):
        try:
            return json.loads(msg)
        except:
            print("error occurs when parse json: %s" % msg)
            sys.exit(-1)

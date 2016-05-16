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

    def startTransaction(self, resource, quantity):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'transaction', 'type': 'startTransaction', 'resource':resource, 'quantity': quantity}
        return json.dumps(msg)

    def confirmStartTransaction(self, resource, quantity):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'transaction', 'type': 'confirmStartTransaction', 'resource':resource, 'quantity': quantity}
        return json.dumps(msg)

    def finishTransaction(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'transaction', 'type': 'finishTransaction'}
        return json.dumps(msg)

    def confirmFinishTransaction(self):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'transaction', 'type': 'confirmFinishTransaction'}
        return json.dumps(msg)

    def buyResource(self, resource, quantity):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'transaction', 'type': 'buyResource', 'resource':resource, 'quantity': quantity}
        return json.dumps(msg)

    def sellResource(self, resource, quantity):
        msg = {'uuid': self.__uuid, 'port': self.__port, 'level': 'transaction', 'type': 'sellResource', 'resource':resource, 'quantity': quantity}
        return json.dumps(msg)

    def parse(self, msg):
        try:
            return json.loads(msg)
        except:
            print("error occurs when parse json: %s" % msg)
            sys.exit(-1)

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

    def parse(self, msg):
        try:
            return json.loads(msg)
        except:
            print("error occurs when parse json: %s" % msg)
            sys.exit(-1)

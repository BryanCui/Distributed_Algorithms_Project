import json
import sys

class Message:

    def __init__(self, uuid):
        self.__uuid = uuid

    def requireNodeList(self):
        msg = {'uuid': self.__uuid, 'level': 'app', 'type': 'requireNodeList'}
        return json.dumps(msg)

    def provideNodeList(self, list):
        msg = {'uuid': self.__uuid, 'level': 'app', 'type': 'provideNodeList', 'list': list}
        return json.dumps(msg)

    def parse(self, msg):
        try:
            return json.loads(msg)
        except:
            print("error occurs when parse json: %s" % msg)
            sys.exit(-1)

from utils import sendmsg
import threading
import sys
from command_record import SEND

# client
class Sender(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port

    # main execution
    def run(self):
        while True:
            line = sys.stdin.readline()
            print sendmsg('127.0.0.1',2334,line)
            print line

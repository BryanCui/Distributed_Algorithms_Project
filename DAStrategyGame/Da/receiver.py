import threading
import json
import socket
import threading

class Receiver(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.address = ('0.0.0.0', 2334)
        # initialize socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # s = socket.socket()
        self.s.bind(self.address)
        self.s.listen(5)
        self.cl_list = []

    def run(self):
        while True:
            cl, addr = self.s.accept()
            self.cl_list.append()
            print 'got connected from',addr[0]

            node_list = dict()
            if addr[0] not in node_list:
                node_list[addr[0]] = 0
            ra = cl.recv(512)
            for item in self.cl_list:
                item.send(str(cl))

            ra = json.loads(ra)
            print ra

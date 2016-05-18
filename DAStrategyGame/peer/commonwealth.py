#coding=UTF-8

import sys, thread, time, logging
import threading
from bank import Bank
import node
'''
__author__ = 'Da'

'''
router = node.router
router[('app', 'activate')] = 'onActivate'

logging.getLogger().setLevel(logging.INFO)

'''
Bank node persists to provide service
__author

'''
class BankNode(node.Node):
    def __init__(self, nickname, port):
        # over
        super(BankNode, self).__init__(nickname,port,'bank')
        thread.start_new_thread(self.node_main, ())
        self.bank = Bank()
        self.cl_list = []
        self.addr_list = []
        self.mylock = threading.RLock()

    # method to activate the cdKey as the node requests
    def onActivate(self, socket, addr, node, msg):
        # activate the cdkey
        self.mylock.acquire()
        result = self.bank.activate_cdkey(msg['cdkey'])
        # sleep for concurrent test
        # time.sleep(5)
        # if it is num
        if not self.is_num(result):
            socket.send(self.msg.answerActivate(balance=result))
        # if it is not num, then error.
        else:
            socket.send(self.msg.answerActivate(info=result))
        logging.info('%s'%result)
        self.mylock.release()

    # re-write the listen method maintaining queue for waiting
    def listen(self):
        while True:
            logging.info('Listening...')
            try:
                logging.info(self)
                client, addr = self._server.accept()
                logging.info('connection from: %s:%d' % (addr[0], addr[1]))
                self.cl_list.append(client)
                self.addr_list.append(addr)
            except KeyboardInterrupt:
                break

    # new method to handle the listener in queue by order
    def node_main(self):
        while True:
            if self.cl_list and self.addr_list:
                self.handle_client(self.cl_list[0], self.addr_list[0])
                del(self.cl_list[0])
                del (self.addr_list[0])
    # Not Num : True; Num: False
    def is_num(self, argv):
        for i in range(len(argv)):
            if not '0' <= argv[i] <= '9':
                return True
        return False

def main(argv):
    print router
    print BankNode.__dict__
    node = BankNode(argv[1], int(argv[2]))
    # for debug only
    while True:
        line = sys.stdin.readline()
        ws = line.split()

        # create cdkey
        if ws[0] == "create" and len(ws)==3:
            node.mylock.acquire()
            if node.is_num(ws[2]):
                logging.info("balance should be num")
            else:
                logging.info("%s" % node.bank.create_balance(ws[1], ws[2]))
            node.mylock.release()

        # delete cdkey
        elif ws[0] == "delete" and len(ws)==2:
            node.mylock.acquire()
            logging.info("%s"%node.bank.delete_balance(ws[1]))
            node.mylock.release()

        # get cdkey list
        elif ws[0] == "list" and len(ws)==1:
            logging.info("we have the available list as: %s" % node.bank.cdkey_list)

        elif ws[0] == 'nodelist':
            logging.info('current local node list: %s' % node.nodeList)

        # send msg
        elif ws[0] == "activate" and len(ws)==4:
            node.send_message((ws[1], int(ws[2])), node.msg.activateCdkey(ws[3]))

        # send msg
        elif ws[0] == "import" and len(ws) == 2:
            node.mylock.acquire()
            logging.info("%s"%node.bank.insertCdkeys(ws[1]))
            node.mylock.release()
        # other commands are wrong
        else:
            print "wrong command"


if __name__ == '__main__':
    main(sys.argv)
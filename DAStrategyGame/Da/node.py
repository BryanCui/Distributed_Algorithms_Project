#coding=utf-8
# server
import json
import socket
import sys


# local host, port
address = ('0.0.0.0', 2333)

#initialize socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
s.bind(address)
s.listen(5)

# main list of nodes.
node_list = dict()
while True:
    cl, addr = s.accept()
    print 'got connected from',addr[0]
    if addr[0] not in node_list:
        node_list[addr[0]] = 0
    print node_list
    print "指导价格"
    ra = cl.recv(512)
    # if some commands comes
    ra = json.loads(ra)
    if ra['command'] == 'chishi':
        cl.send('chishi')


cl.close()
s.close()

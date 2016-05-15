# server

import socket

# local host, port
address = ('127.0.0.1', 31500)

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
    cl.send('byebye')
    ra = cl.recv(512)
    print ra

cl.close()
s.close()

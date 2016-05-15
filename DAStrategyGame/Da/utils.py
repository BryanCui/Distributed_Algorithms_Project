import socket
import json
# send msg to target
def sendmsg(ip, port, msg):
    address = (ip, port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)
    msg = json.dumps(msg)
    s.send(msg)
    result = s.recv(512)
    s.close()
    return result
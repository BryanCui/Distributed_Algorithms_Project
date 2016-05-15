from utils import sendmsg
# client

msg = dict(command="chishi")

for i in range(0,10):
    print sendmsg('127.0.0.1',2333,msg)


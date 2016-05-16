from receiver import Receiver
from sender import Sender

if __name__ == '__main__':
    t2 = Sender('127.0.0.1',2334)
    t2.start()
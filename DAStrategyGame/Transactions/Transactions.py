#Transactions
import message
import time

UUID = int(round(time.time() * 1000))
MSG = message.Message(UUID)

class Transaction:
    def __init__(self, host, node):
        self.__host = host
        self.__node = node


    def start_transaction(self):
        message
        self.__node.send_message(self, self.__host, MSG.)

    def end_transaction(self):


    def buy_resource(self):


    def sell_resource(self):




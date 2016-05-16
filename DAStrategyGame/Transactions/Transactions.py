#Transactions
import message
import time

UUID = int(round(time.time() * 1000))


class Transaction:
    def __init__(self, host, node):
        self.__host = host
        self.__node = node
        self.__MSG = message.Message(UUID)


    def start_transaction(self):
        self.__node.send_message(self, self.__host, self.__MSG.startTransaction())


    def end_transaction(self):


    def buy_resource(self):


    def sell_resource(self):




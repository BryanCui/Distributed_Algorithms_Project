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
        self.__node.send_message(self, self.__host, self.__MSG.finishTransaction())

    def buy_resource(self, resource, quantity):
        self.__node.send_message(self, self.__host, self.__MSG.buyResource(self, resource, quantity))

    def sell_resource(self, resource, quantity):
        self.__node.send_message(self, self.__host, self.__MSG.sellResource(self, resource, quantity))



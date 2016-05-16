#Transactions
import message
import time, socket

UUID = int(round(time.time() * 1000))


class Transaction:
    __food = 0
    __wood = 0
    __mineral = 0
    __leather = 0
    __money = 0
    def __init__(self, host, msg, node, user):
        self.__host = host
        self.__node = node
        self.__MSG = msg
        self.__user = user


    def start_transaction(self):
        self.__node.send_message(self, self.__host, self.__MSG.startTransaction())

    def end_transaction(self):
        self.__node.send_message(self, self.__host, self.__MSG.finishTransaction())

    def buy_resource(self, resource, quantity):
        self.__node.send_message(self, self.__host, self.__MSG.buyResource(self, resource, quantity))
        self.__user.add_resources(resource, quantity)
        self.__user.consume_money(resource.getPrice() * quantity)

    def sell_resource(self, resource, quantity):
        self.__node.send_message(self, self.__host, self.__MSG.sellResource(self, resource, quantity))
        self.__user.consume_resources(resource, quantity)
        self.__user.add_money(resource.getPrice() * quantity)

    def set_transaction_status(self, user):
        self.__food = user.get_food()
        self.__wood = user.get_wood()
        self.__mineral = user.get_mineral()
        self.__leather = user.get_leather()
        self.__money = user.get_money()

    def recover_transaction_status(self, user):
        self.__user.set_resources(self.__food, self.__wood, self.__mineral, self.__leather, self.__money)
        return self.__user









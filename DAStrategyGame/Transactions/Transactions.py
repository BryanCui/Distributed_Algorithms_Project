# Transactions

from User.Resource import *


class Transactions:
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

    def start_transaction(self, resource, quantity):
        self.__node.send_message(self.__host, self.__MSG.startTransaction(resource, quantity))

    def confirm_start_transaction(self, socket, resource, quantity):
        socket.send(self.__MSG.confirmStartTransaction(resource, quantity))

    def finish_transaction(self, addr, msg):
        resource = msg['resource']
        quantity = msg['quantity']
        price = msg['price']
        self.__user.consume_money(int(price) * quantity)
        self.__node.send_message(addr, self.__MSG.finishTransaction())

    def confirm_finish_transaction(self, socket):
        socket.send(self.__MSG.confirmFinishTransaction())

    def buy_resource(self, addr, resource, quantity):
        self.__user.add_resources(resource, quantity)
        #self.__user.consume_money(self.__user.get_trading_center().earn_money(resource, quantity))
        self.__node.send_message(addr, self.__MSG.buyResource(resource, quantity))

    def sell_resource(self, socket, resource, quantity, price):
        self.__user.get_trading_center().consume_resources(resource, quantity)
        self.__user.add_money(int(price) * quantity)
        socket.send(self.__MSG.sellResource(resource, quantity, self.__user.get_trading_center().get_resources_price(resource)))

    def set_transaction_status(self, user):
        self.__food = user.get_food()
        self.__wood = user.get_wood()
        self.__mineral = user.get_mineral()
        self.__leather = user.get_leather()
        self.__money = user.get_money()

    def set_transaction_status(self, trading_center):
        self.__food = trading_center.get_food()
        self.__wood = trading_center.get_wood()
        self.__mineral = trading_center.get_mineral()
        self.__leather = trading_center.get_leather()

    def recover_transaction_status_buy(self):
        self.__user.set_resources(self.__food, self.__wood, self.__mineral, self.__leather, self.__money)
        return self.__user

    def recover_transaction_status_sell(self, trading_center):
        trading_center.set_resources(self.__food, self.__wood, self.__mineral, self.__leather, self.__money)
        return self.__user



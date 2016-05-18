# Transactions

from User.Resource import *
from Singleton import Singleton
import threading
from time import sleep


class Transactions(Singleton):
    __food = 0
    __wood = 0
    __mineral = 0
    __leather = 0
    __trading_food = 0
    __trading_wood = 0
    __trading_mineral = 0
    __trading_leather = 0
    __money = 0

    def __init__(self, host, msg, node, user):
        self.__host = host
        self.__node = node
        self.__MSG = msg
        self.__user = user
        self.__is_finished = False

    def start_transaction(self, resource, quantity):
        self.set_user_status(self.__user)
        self.set_trading_status(self.__user.get_trading_center())
        self.__node.send_message(self.__host, self.__MSG.startTransaction(resource, quantity))
        self.transaction_thread()

    def confirm_start_transaction(self, socket, resource, quantity):
        self.set_user_status(self.__user)
        self.set_trading_status(self.__user.get_trading_center())
        socket.send(self.__MSG.confirmStartTransaction(resource, quantity))
        self.transaction_thread()

    def finish_transaction(self, addr, msg):
        resource = msg['resource']
        quantity = msg['quantity']
        price = msg['price']
        self.__user.consume_money(int(price) * quantity)
        self.__node.send_message(addr, self.__MSG.finishTransaction())

    def confirm_finish_transaction(self, socket):
        socket.send(self.__MSG.confirmFinishTransaction())

    def done_transaction(self, addr):
        self.__node.send_message(addr, self.__MSG.doneTransaction())

    def buy_resource(self, addr, resource, quantity):
        self.__user.add_resources(resource, quantity)
        self.__node.send_message(addr, self.__MSG.buyResource(resource, quantity))

    def sell_resource(self, socket, resource, quantity, price):
        self.__user.get_trading_center().consume_resources(resource, quantity)
        self.__user.add_money(int(price) * quantity)
        socket.send(self.__MSG.sellResource(resource, quantity, self.__user.get_trading_center().get_resources_price(resource)))

    def set_user_status(self, user):
        self.__food = user.get_food()
        self.__wood = user.get_wood()
        self.__mineral = user.get_mineral()
        self.__leather = user.get_leather()
        self.__money = user.get_money()

    def set_trading_status(self, trading_center):
        self.__trading_food = trading_center.get_food()
        self.__trading_wood = trading_center.get_wood()
        self.__trading_mineral = trading_center.get_mineral()
        self.__trading_leather = trading_center.get_leather()

    def recover_transaction_status_buy(self):
        self.__user.set_resources(self.__food, self.__wood, self.__mineral, self.__leather, self.__money)

    def recover_transaction_status_sell(self):
        self.__user.get_trading_center().set_resources(self.__trading_food, self.__trading_wood, self.__trading_mineral, self.__trading_leather)

    def set_finished(self, finished):
        self.__is_finished = finished

    def get_finished(self):
        return self.__is_finished

    def transaction_thread(self):
        transaction_thread = threading.Thread(target=self.transaction_success_fail())
        transaction_thread.start()

    def transaction_success_fail(self):
        sleep(6)
        if not self.get_finished():
            self.recover_transaction_status_buy()
            self.recover_transaction_status_sell()
            self.set_finished(False)





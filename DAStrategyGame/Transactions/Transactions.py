# Transactions

from User.Resource import *


class Transaction:
    __food = 0
    __wood = 0
    __mineral = 0
    __leather = 0
    __money = 0
    __transaction_status = ['', False]

    def __init__(self, host, msg, node, user, tradingCenter):
        self.__host = host
        self.__node = node
        self.__MSG = msg
        self.__user = user
        self.__tradingCenter = tradingCenter

    def start_transaction(self):
        self.__node.send_message(self, self.__host, self.__MSG.startTransaction())

    def confirm_start_transaction(self):
        self.__node.send_message(self, self.__host, self.__MSG.confirmStartTransaction())

    def end_transaction(self):
        self.__node.send_message(self, self.__host, self.__MSG.finishTransaction())

    def confirm_end_transaction(self):
        self.set_transaction_finished_status(True)
        self.__node.send_message(self, self.__host, self.__MSG.confirmFinishTransaction())

    def buy_resource(self, resource, quantity):
        self.set_transaction_status('buy')
        self.set_transaction_finished_status(False)

        self.__node.send_message(self, self.__host, self.__MSG.buyResource(self, resource, quantity))
        self.__user.add_resources(resource, quantity)
        current_resource = Resource(resource)
        self.__user.consume_money(current_resource.getPrice() * quantity)

    def sell_resource(self, resource, quantity):
        self.set_transaction_status('sell')
        self.set_transaction_finished_status(False)

        self.__node.send_message(self, self.__host, self.__MSG.sellResource(self, resource, quantity))
        current_resource = Resource(resource)
        self.__tradingCenter.consume_resources(resource, quantity)
        self.__user.add_money(current_resource.getPrice() * quantity)

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

    def recover_transaction_status_sell(self):
        self.__tradingCenter.set_resources(self.__food, self.__wood, self.__mineral, self.__leather, self.__money)
        return self.__user

    def set_transaction_status(self, transaction_type):
        self.__transaction_status[0] = transaction_type

    def set_transaction_finished_status(self, is_done):
        self.__transaction_status[1] = is_done

    def get_transaction_status(self):
        return self.__transaction_status

    def put_resource_into_trading_center(self, resource, quantity, price):
        self.__tradingCenter.set_resource_to_sell(resource, quantity, price)
        self.__user.consume_resources(resource, quantity)

    def get_resource_from_trading_center(self, resource, quantity):
        self.__tradingCenter.consume_resources(resource, quantity)
        self.__user.add_resources(resource, quantity)
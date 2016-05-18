# user


from TradingCenter import TradingCenter
from Singleton import Singleton
from time import sleep
import thread


class User(Singleton):
    def __init__(self, role):
        self.__food = 1000
        self.__wood = 1000
        self.__mineral = 1000
        self.__leather = 1000
        self.__money = 10000
        self.__role = role
        self.__trading_center = TradingCenter()
        self.food_consuming_thread()
        self.role_thread(self.__role)

    @property
    def trading_center(self):
        return self.__trading_center

    def set_resources(self, food, wood, mineral, leather, money):
        self.__food = food
        self.__wood = wood
        self.__mineral = mineral
        self.__leather = leather
        self.__money = money

    def add_food(self, quantity):
        self.__food += quantity

    def consume_food(self, quantity):
        self.__food -= quantity

    def get_food(self):
        return self.__food

    def add_wood(self, quantity):
        self.__wood += quantity

    def consume_wood(self, quantity):
        self.__wood -= quantity

    def get_wood(self):
        return self.__wood

    def add_mineral(self, quantity):
        self.__mineral += quantity

    def consume_mineral(self, quantity):
        self.__mineral -= quantity

    def get_mineral(self):
        return self.__mineral

    def add_leather(self, quantity):
        self.__leather += quantity

    def consume_leather(self, quantity):
        self.__leather -= quantity

    def get_leather(self):
        return self.__leather

    def add_money(self, quantity):
        self.__money += quantity

    def consume_money(self, quantity):
        self.__money -= quantity

    def get_money(self):
        return self.__money

    def add_resources(self, resource, quantity):
        if resource == 'food':
            self.add_food(quantity)
        elif resource == 'wood':
            self.add_wood(quantity)
        elif resource == 'mineral':
            self.add_mineral(quantity)
        elif resource == 'leather':
            self.add_leather(quantity)
        else:
            print 'Wrong resource name!'
            return

    def consume_resources(self, resource, quantity):
        if resource == 'food':
            self.consume_food(quantity)
        elif resource == 'wood':
            self.consume_wood(quantity)
        elif resource == 'mineral':
            self.consume_mineral(quantity)
        elif resource == 'leather':
            self.consume_leather(quantity)
        else:
            return

    def show_resources(self):
        print 'Food: %d' % self.__food
        print 'Wood: %d' % self.__wood
        print 'Mineral: %d' % self.__mineral
        print 'Leather: %d' % self.__leather
        print 'Money: %d' % self.__money




    def put_resource_into_trading_center(self, resource, quantity, price):
        self.__trading_center.set_resource_to_sell(resource, quantity, price)
        self.consume_resources(resource, quantity)

    def get_resource_from_trading_center_back(self, resource, quantity):
        self.__trading_center.consume_resources(resource, quantity)
        self.add_resources(resource, quantity)

    def get_user_resource_status(self):
        return {
            'food': self.__food,
            'wood': self.__wood,
            'mineral': self.__mineral,
            'leather': self.__leather,
            'money': self.__money
        }

    def get_trading_center_status(self):
        return {
            'food': (self.trading_center.get_food(), self.trading_center.get_food_price()),
            'wood': (self.trading_center.get_wood(), self.trading_center.get_wood_price()),
            'mineral': (self.trading_center.get_mineral(), self.trading_center.get_mineral_price()),
            'leather': (self.trading_center.get_leather(), self.trading_center.get_leather_price())
        }

    def food_consuming_thread(self):
        thread.start_new_thread(self.food_consuming, ())

    def food_consuming(self):
        while True:
            sleep(15)
            self.__food -= 1

    def role_thread(self, role):
        thread.start_new_thread(self.role_character, ())

    def role_character(self):
        if self.__role == 'farmer':
            while True:
                sleep(10)
                self.__food += 5
        elif self.__role == 'lumberjack':
            while True:
                sleep(10)
                self.__wood += 5
        elif self.__role == 'miner':
            while True:
                sleep(10)
                self.__mineral += 5
        elif self.__role == 'fellmonger':
            while True:
                sleep(10)
                self.__leather += 5

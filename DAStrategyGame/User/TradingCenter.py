#Trading Center

from Singleton import Singleton


class TradingCenter(Singleton):

    def __init__(self):
        self.__food = [0, 0]
        self.__wood = [0, 0]
        self.__mineral = [0, 0]
        self.__leather = [0, 0]

    def set_resource_to_sell(self, resource, quantity, price):
        if resource == 'food':
            self.__food = [self.__food[0]+quantity, price]
        elif resource == 'wood':
            self.__wood = [self.__wood[0]+quantity, price]
        elif resource == 'mineral':
            self.__mineral = [self.__mineral[0]+quantity, price]
        elif resource == 'leather':
            self.__leather = [self.__leather[0]+quantity, price]

    def get_food_price(self):
        return self.__food[1]

    def get_wood_price(self):
        return self.__wood[1]

    def get_mineral_price(self):
        return self.__mineral[1]

    def get_leather_price(self):
        return self.__leather[1]

    def set_resources(self, food, wood, mineral, leather):
        self.__food[1] = food
        self.__wood[1] = wood
        self.__mineral[1] = mineral
        self.__leather[1] = leather

    def show_trading_center(self):
        print "Food: %d  Price: %d" % (self.__food[0], self.__food[1])
        print "Wood: %d  Price: %d" % (self.__wood[0], self.__wood[1])
        print "Mineral: %d  Price: %d" % (self.__mineral[0], self.__mineral[1])
        print "Leather: %d  Price: %d" % (self.__leather[0], self.__leather[1])

    def consume_resources(self, resource, quantity):
        if resource == 'food':
            self.__food[0] -= quantity
        elif resource == 'wood':
            self.__wood -= quantity
        elif resource == 'mineral':
            self.__mineral -= quantity
        elif resource == 'leather':
            self.__leather -= quantity

    def earn_money(self, resource, quantity):
        if resource == 'food':
            money = quantity * self.get_food_price()
        elif resource == 'wood':
            money = quantity * self.get_wood_price()
        elif resource == 'mineral':
            money = quantity * self.get_mineral_price()
        elif resource == 'leather':
            money = quantity * self.get_leather_price()
        return money

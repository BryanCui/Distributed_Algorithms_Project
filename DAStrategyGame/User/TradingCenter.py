#Trading Center

from Singleton import Singleton
import logging


class TradingCenter(Singleton):

    def __init__(self):
        # [quantity, price, resource_name]
        self.__food = [0, 0, 'food']
        self.__wood = [0, 0, 'wood']
        self.__mineral = [0, 0, 'mineral']
        self.__leather = [0, 0, 'leather']

    # set the resources to sell
    def set_resource_to_sell(self, resource, quantity, price):
        if resource == 'food':
            self.__food = [self.__food[0]+quantity, price, 'food']
        elif resource == 'wood':
            self.__wood = [self.__wood[0]+quantity, price, 'wood']
        elif resource == 'mineral':
            self.__mineral = [self.__mineral[0]+quantity, price, 'mineral']
        elif resource == 'leather':
            self.__leather = [self.__leather[0]+quantity, price, 'leather']

    def get_food_price(self):
        return self.__food[1]

    def get_wood_price(self):
        return self.__wood[1]

    def get_mineral_price(self):
        return self.__mineral[1]

    def get_leather_price(self):
        return self.__leather[1]

    def get_food(self):
        return self.__food[0]

    def get_wood(self):
        return self.__wood[0]

    def get_mineral(self):
        return self.__mineral[0]

    def get_leather(self):
        return self.__leather[0]

    # get the resource price according to the resource name
    def get_resources_price(self, resource):
        if resource == 'food':
            return self.__food[1]
        elif resource == 'wood':
            return self.__wood[1]
        elif resource == 'mineral':
            return self.__mineral[1]
        elif resource == 'leather':
            return self.__leather[1]

    # get the resource quantity according to the resource name
    def get_resources(self, resource):
        if resource == 'food':
            return self.__food[0]
        elif resource == 'wood':
            return self.__wood[0]
        elif resource == 'mineral':
            return self.__mineral[0]
        elif resource == 'leather':
            return self.__leather[0]
        else:
            logging.info('Wrong resource name!')
            return

    def set_resources(self, food, wood, mineral, leather):
        self.__food[0] = food
        self.__wood[0] = wood
        self.__mineral[0] = mineral
        self.__leather[0] = leather

    # show the trading center status
    def show_trading_center(self):
        logging.info("Food: %d  Price: %d" % (self.__food[0], self.__food[1]))
        logging.info("Wood: %d  Price: %d" % (self.__wood[0], self.__wood[1]))
        logging.info("Mineral: %d  Price: %d" % (self.__mineral[0], self.__mineral[1]))
        logging.info("Leather: %d  Price: %d" % (self.__leather[0], self.__leather[1]))

    # consume the resources from trading center
    def consume_resources(self, resource, quantity):
        if resource == 'food':
            self.__food[0] -= quantity
        elif resource == 'wood':
            self.__wood[0] -= quantity
        elif resource == 'mineral':
            self.__mineral[0] -= quantity
        elif resource == 'leather':
            self.__leather[0] -= quantity

    # def earn_money(self, resource, quantity):
    #     if resource == 'food':
    #         money = quantity * self.get_food_price()
    #     elif resource == 'wood':
    #         money = quantity * self.get_wood_price()
    #     elif resource == 'mineral':
    #         money = quantity * self.get_mineral_price()
    #     elif resource == 'leather':
    #         money = quantity * self.get_leather_price()
    #     return money

    # get the trading center resources and price
    def get_trading_list(self):
        return {'food':(self.__food[0], self.__food[1]),
                'wood':(self.__wood[0], self.__wood[1]),
                'mineral':(self.__mineral[0], self.__mineral[1]),
                'leather':(self.__leather[0], self.__leather[1])}

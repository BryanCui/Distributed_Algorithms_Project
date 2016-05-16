# user

class User:
    def __init__(self):
        self.__food = 1000
        self.__wood = 1000
        self.__mineral = 1000
        self.__leather = 1000
        self.__money = 10000

    def add_food(self, quantity):
        self.__food += quantity

    def comsume_food(self, quantity):
        self.__food -= quantity

    def add_wood(self, quantity):
        self.__wood += quantity

    def comsume_wood(self, quantity):
        self.__wood -= quantity

    def add_mineral(self, quantity):
        self.__mineral += quantity

    def comsume_mineral(self, quantity):
        self.__mineral -= quantity

    def add_leather(self, quantity):
        self.__leather += quantity

    def comsume_leather(self, quantity):
        self.__leather -= quantity

    def add_money(self, quantity):
        self.__money += quantity

    def comsume_money(self, quantity):
        self.__money -= quantity

    def show_resources(self):
        print 'Food: %d' % self.__food
        print 'Wood: %d' % self.__wood
        print 'Mineral: %d' % self.__mineral
        print 'Leather: %d' % self.__leather
        print 'Money: %d' % self.__money

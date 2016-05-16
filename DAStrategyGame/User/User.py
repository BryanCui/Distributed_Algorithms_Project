# user

class User:
    def __init__(self):
        self.__food = 1000
        self.__wood = 1000
        self.__mineral = 1000
        self.__leather = 1000
        self.__money = 10000

    def set_resources(self, food, wood, mineral, leather, money):
        self.__food = food
        self.__wood = wood
        self.__mineral = mineral
        self.__leather = leather
        self.__money = money

    def add_food(self, quantity):
        self.__food += quantity

    def comsume_food(self, quantity):
        self.__food -= quantity

    def get_food(self):
        return self.__food

    def add_wood(self, quantity):
        self.__wood += quantity

    def comsume_wood(self, quantity):
        self.__wood -= quantity

    def get_wood(self):
        return self.__wood

    def add_mineral(self, quantity):
        self.__mineral += quantity

    def comsume_mineral(self, quantity):
        self.__mineral -= quantity

    def get_mineral(self):
        return self.__mineral

    def add_leather(self, quantity):
        self.__leather += quantity

    def comsume_leather(self, quantity):
        self.__leather -= quantity

    def get_leather(self):
        return self.__leather

    def add_money(self, quantity):
        self.__money += quantity

    def comsume_money(self, quantity):
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

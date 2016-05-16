# Resource
class Resource:
    __current_resource = ''
    __current_price = 0

    def __init__(self, resource):
        if resource == 'food':
            self.__current_resource = 'food'
        if resource == 'wood':
            self.__current_resource = 'wood'
        if resource == 'mineral':
            self.__current_resource = 'mineral'
        if resource == 'leather':
            self.__current_resource = 'leather'

    def get_resource_name(self):
        return self.__current_resource

    def set_price(self, price):
        self.__current_price = price

    def get_price(self):
        return self.__current_price

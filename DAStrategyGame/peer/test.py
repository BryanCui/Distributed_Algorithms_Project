class Base(object):
    def __init__(self, a):
        self._a = a

    def p(self):
        print(self._a)
        print(type(self).__name__)
        print(globals())

class Haha(Base):
    def __init__(self, a):
        super(Haha, self).__init__(a)
        self._a = a + 1

h = Haha(2)
h.p()
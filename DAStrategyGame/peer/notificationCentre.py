# coding=UTF-8

class NotificationCentre(object):
    centre = None

    # callback = {
    #     'event': [
    #         {'func': func, 'obj': obj},
    #         ...
    #     ],
    #     ...
    # }

    # func(self, info:dict)

    def __init__(self):
        self._callback = {}

    @classmethod
    def defaultCentre(cls):
        if cls.centre == None:
            cls.centre = NotificationCentre()
        return cls.centre

    def addObserver(self, event, target, callback):
        arr = self._callback.get(event, [])
        arr.append({'func': callback, 'obj': target})
        self._callback[event] = arr

    def removeObserver(self, event, target):
        arr = self._callback.get(event, [])
        for item in arr:
            if item['obj'] == target:
                arr.remove(item)
        self._callback[event] = arr

    def fire(self, event, info):
        arr = self._callback.get(event, [])
        for item in arr:
            cls = item['obj'].__class__
            func = cls.__dict__[item['func']]
            apply(func, (item['obj'], info))
            
#!/usr/bin/env python
# encoding: utf-8

import npyscreen

class MainScreen(npyscreen.SplitForm):

    def __init__(self, name):
        npyscreen.SplitForm.__init__(self, name="Tradercraft " + name)

        self.MOVE_LINE_ON_RESIZE = True

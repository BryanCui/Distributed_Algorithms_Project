#!/usr/bin/env python
# encoding: utf-8

import npyscreen

class LoginScreen(npyscreen.Form):

    def __init__(self):
        npyscreen.Form.__init__(self, name = "Tradercraft Login")

        # nickname = self.add_widget(TextBox, name="Nick Name")

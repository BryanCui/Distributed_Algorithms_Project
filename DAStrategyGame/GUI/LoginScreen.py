#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import random

class LoginScreen(npyscreen.ActionForm):

    def __init__(self):
        npyscreen.ActionForm.__init__(self, name = "Tradercraft Login")

        # introduce message
        self.add_widget(npyscreen.FixedText
            , value="Welcome to the Tradercraft, you should input a nickname to play"
            , editable=False)
        self.add_widget(npyscreen.FixedText
            , value=""
            , editable=False)

        # login form
        self.nickname = self.add_widget(npyscreen.TitleText, name="Nick Name"
            , value="trader" + str(random.randint(100, 999)))
        self.address = self.add_widget(npyscreen.TitleText
            , name="Server address"
            , value="0.0.0.0:5556")
        self.listenport = self.add_widget(npyscreen.TitleText
            , name="Listen to"
            , value="5556")

        self.add_widget(npyscreen.FixedText
            , value=""
            , editable=False)

        # select role
        self.role = self.add(npyscreen.TitleSelectOne
            , max_height=8
            , value = [0,]
            , name="Pick your role"
            , values = [
                "Farmer"
                ,"Miner"
                ,"Hunter"
                ,"Handicraftsman"
                ,"Tailor"
                ,"Blacksmith"
                ,"Timberjack"
            ]
            , scroll_exit=True)

    def on_ok(self):
        self.move_forward = True;

    def on_cancel(self):
        self.move_forward = False;


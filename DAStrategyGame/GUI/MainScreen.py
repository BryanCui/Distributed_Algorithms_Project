#!/usr/bin/env python
# encoding: utf-8

import npyscreen
import types

class MainScreen(npyscreen.Form):

    def __init__(self, name):
        npyscreen.Form.__init__(self, name="Tradercraft " + name)

        self.add_widget(npyscreen.FixedText
            , value="You have:"
            , editable=False)

        self.inventoryText = self.add_widget(npyscreen.MultiLineEdit
            , value=self.getPlayerIventory()
            , max_height=3
            , editable=False)

        self.add_widget(npyscreen.FixedText
            , value=""
            , editable=False)

        self.peopleSelection = self.add(npyscreen.TitleSelectOne
            , max_height=5
            , name="People around you:"
            , values = [
                "People 1"
                ,"People 2"
                ,"People 3"
                ,"People 4"
                ,"People 5"
                ,"People 6"
                ,"People 7"
            ]
            , scroll_exit=True)

        self.peopleSelection.actionHighlighted = types.MethodType(self.action, self.peopleSelection)

    # get the player's inventory in formatted string
    def getPlayerIventory(self):
        return '''
         Gold: 1000     Iron: 10
         Wood: 50       Food: 0
        '''

    def action(self, act_on_this, key_press):
        popup = npyscreen.Popup(name="I am clicked")
        popup.edit()


#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from PeopleList import PeopleList

from peer.command import Command

class MainScreen(npyscreen.Form):

    def __init__(self, name, command):
        npyscreen.Form.__init__(self, name="Tradercraft " + name)

        self.inventoryText = self.add_widget(npyscreen.MultiLineEdit
            , value=self.getPlayerIventory()
            , color='STANDOUT'
            , max_height=3
            , editable=False)

        self.add_widget(npyscreen.FixedText
            , relx=50
            , rely=2
            , value="7 People around you"
            , color='IMPORTANT'
            , editable=False)

        self.peopleSelection = self.add(PeopleList
            , relx=50
            , rely=3
            , max_height=5
            , scroll_exit=True)

        self.refreshBtn = self.add_widget(npyscreen.Button
            , relx=49
            , rely=9
            , when_pressed_function=self.lookaround
            , name="Look around")

        self.command = command
        self.lookaround()

    #refresh the people around you
    def lookaround(self):
        popup = npyscreen.Popup(name="I am clicked")
        popup.edit()
        list = []
        for people in self.command.execute('localNodeList'):
            list.append(people[3])
        self.peopleSelection.values=list

    # get the player's inventory in formatted string
    def getPlayerIventory(self):
        return '''
Gold: 1000     Iron: 10
Wood: 50       Food: 0
'''

#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from Component import *

from peer.command import Command

class MainScreen(npyscreen.Form):

    def __init__(self, name, command):
        npyscreen.Form.__init__(self, name="Tradercraft " + name)

        self.inventoryText = self.add_widget(npyscreen.MultiLineEdit
            , value=self.getPlayerIventory()
            , color='STANDOUT'
            , max_height=3
            , editable=False)

        self.peoplenote = self.add_widget(npyscreen.FixedText
            , relx=50
            , rely=2
            , color='IMPORTANT'
            , editable=False)

        self.peopleSelection = self.add(PeopleList
            , relx=50
            , rely=3
            , max_height=5
            , scroll_exit=True)

        self.refreshBtn = self.add_widget(RefreshBtn
            , relx=49
            , rely=9
            , name="Look around")

        self.command = command
        self.lookAround()

    #refresh the people around you
    def lookAround(self):
        list = []
        for people in self.command.execute('localNodeList'):
            list.append(people[3] + " the " + people[4])
        self.peopleSelection.values=list
        self.peoplenote.value = str(len(list)) + " people around you:"
        self.display()

    # get the player's inventory in formatted string
    def updateIventory(self):
        list = []
        for resource in self.command.execute('localResource'):
            list.append()

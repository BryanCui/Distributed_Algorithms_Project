#!/usr/bin/env python
# encoding: utf-8

import sys
import npyscreen

from GUI.LoginScreen import LoginScreen

from peer.command import Command
from peer.notificationCentre import NotificationCentre

class ActionControllerCmd(npyscreen.ActionControllerSimple):
    def create(self):
        self.add_action('^.*', self.handle, False)

    def handle(self, command_line, widget_proxy, live):
        commands = command_line.split()

        commands[0] = commands[0][1:]

        if commands[0] == "q":
            sys.exit() 

        App.updateInfo()

        if commands[0] != "r":
            self.parent.wMain.values.append(App.command.execute(commands[0], commands[1:]))
        self.parent.wMain.display()

class CommandActive(npyscreen.FormMuttActiveTraditional):
    ACTION_CONTROLLER = ActionControllerCmd

class App(npyscreen.NPSApp):

    # main entry of the App
    def main(self):

        self.command = Command()

        # loop until cancel or successfully login
        while True:
            self.loginScreen  = LoginScreen()
            self.loginScreen.edit()

            if not self.loginScreen.move_forward:    # select cancel
                return

            self.nickname = self.loginScreen.nickname.value
            self.address = self.loginScreen.address.value
            self.listenport = self.loginScreen.listenport.value
            self.role = self.loginScreen.role.get_selected_objects()[0];

            if not self.setup():
                popup = npyscreen.Popup(name="Login failed")
                popup.add_widget(npyscreen.FixedText
                    , value="Please check the address and try again later"
                    , editable=False)
                popup.edit()
            else:
                break

        #main screen
        self.c = CommandActive()
        self.c.wStatus1.value = "[" + self.nickname + " as " + self.role + "]"
        self.updateInfo()
        self.c.edit()

        NotificationCentre.defaultCentre().addObserver('event', self, updateInfo)

        self.command.execute('logout')

    # setup the node
    def setup(self):
        if self.address.split(":")[0] == "0.0.0.0":
            return self.launch(self.listenport);
        else:
            return self.login(self.address)

    # login to remote server
    def login(self, address):
        return self.command.execute('joinGame'
            , self.nickname
            , self.role
            , self.listenport
            , (self.address.split(":")[0], int(self.address.split(":")[1])))

    # launch the node itself
    def launch(self, port):
        self.command.execute('createGame'
            , self.nickname
            , self.role
            , int(self.address.split(":")[1]))
        return True

    #refresh the people around you
    def updateInfo(self):
        info = []

        # people around
        count = 0
        for people in self.command.execute('localNodeList'):
            info.append(people[3] + " the " + people[4])
            count += 1

        info.append("There are " + str(count) + " people around you.")
        info.append("------------------------------")

        # local resource
        resourceDict = self.command.execute('localResource')
        info.append("money: " + str(resourceDict['money']['stock']))

        for key in resourceDict.keys():
            if key == 'money':
                continue
            else:
                if resourceDict[key]["for trade"]:
                    info.append(key + ' ' + str(resourceDict[key]['stock']) + " for trade")
                else:
                    info.append(key + ' ' + str(resourceDict[key]['stock']) + " in inventory")

        info.append("------------------------------")
        self.c.wMain.values = info
        self.c.wMain.display()
        

if __name__ == "__main__":
    App = App()
    App.run()

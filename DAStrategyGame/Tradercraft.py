#!/usr/bin/env python
# encoding: utf-8

import sys, logging
import npyscreen

from GUI.LoginScreen import LoginScreen

from peer.command import Command
from peer.notificationCentre import NotificationCentre

logging.basicConfig(filename='log.log',level=logging.DEBUG)

class ActionControllerCmd(npyscreen.ActionControllerSimple):
    def create(self):
        self.add_action('^.*', self.handle, False)

    def handle(self, command_line, widget_proxy, live):
        commands = command_line.split()

        commands[0] = commands[0][1:]

        if commands[0] == "q":
            sys.exit() 

        result = ""
        if commands[0] != "r":
            if len(commands) >= 2: 
                result = App.command.execute(commands[0], *commands[1:])
            else:
                result = App.command.execute(commands[0])

        App.updateInfo()
        self.parent.wMain.values.append(result)

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

        # NotificationCentre.defaultCentre().addObserver('resource_change', self, 'updateInfo')
        # NotificationCentre.defaultCentre().addObserver('trading_change', self, 'updateInfo')
        NotificationCentre.defaultCentre().addObserver('SnapshotDidFinish', self, 'onSnapshot')

        #main screen
        self.c = CommandActive()
        self.c.wStatus1.value = "[" + self.nickname + " as " + self.role + "]"
        self.updateInfo()
        self.c.edit()

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

    #when take snapshot
    def onSnapshot(self, arg):
        self.updateInfo()
        self.c.wMain.values.append(arg['snapshot'].__dict__)
        self.c.wMain.display()

    #refresh the people around you
    def updateInfo(self, arg = None):
        info = []

        # people around
        count = 0
        for people in self.command.execute('nodeList'):
            info.append(people[3] + " the " + people[4] + " @ " + str(people[1]) + ":" + str(people[2]))
            count += 1

        info.append("There are " + str(count) + " people around you.")
        info.append("------------------------------")

        # local resource
        resourceDict = self.command.execute('show')
        info.append("money: " + str(resourceDict['money']['stock']))

        for key in resourceDict.keys():
            if key == 'money':
                continue
            else:
                if resourceDict[key]["for trade"] == 0:
                    info.append(key + ': ' + str(resourceDict[key]['stock']) + " instock")
                else:
                    info.append(key + ': ' + str(resourceDict[key]['for trade']) + " for trade at price " + str(resourceDict[key]['price']) + ", and " + str(resourceDict[key]['stock']) + " in stock.")

        info.append("------------------------------")
        self.c.wMain.values = info
        self.c.wMain.display()
        

if __name__ == "__main__":
    App = App()
    App.run()

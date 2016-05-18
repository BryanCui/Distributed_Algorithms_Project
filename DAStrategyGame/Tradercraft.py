#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from GUI.LoginScreen import LoginScreen
from GUI.MainScreen import MainScreen

from peer.command import Command

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

        # launch main screen
        mainScreen = MainScreen("[" + self.nickname + " as " + self.role + "]", self.command)
        mainScreen.edit();

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

if __name__ == "__main__":
    App = App()
    App.run()

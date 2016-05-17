#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from GUI.LoginScreen import LoginScreen
from GUI.MainScreen import MainScreen

class App(npyscreen.NPSApp):

    # main entry of the App
    def main(self):

        while True:
            loginScreen  = LoginScreen()
            loginScreen.edit()

            if not loginScreen.move_forward:    # select cancel
                return

            nickname = loginScreen.nickname.value
            address = loginScreen.address.value
            role = loginScreen.role.get_selected_objects()[0];

            if not self.connect(address):
                popup = npyscreen.Popup(name="Login failed")
                popup.add_widget(npyscreen.FixedText
                    , value="Please check the address and try again later"
                    , editable=False)
                popup.edit()
            else:
                break

        mainScreen = MainScreen("[" + nickname + " as " + role + "]")
        mainScreen.edit();

    # connect to remote node
    def connect(self, address):
        return False

if __name__ == "__main__":
    App = App()
    App.run()

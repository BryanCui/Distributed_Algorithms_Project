#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from GUI.LoginScreen import LoginScreen
from GUI.MainScreen import MainScreen

class App(npyscreen.NPSApp):

    # main entry of the App
    def main(self):

        # loop until cancel or successfully login
        while True:
            loginScreen  = LoginScreen()
            loginScreen.edit()

            if not loginScreen.move_forward:    # select cancel
                return

            nickname = loginScreen.nickname.value
            address = loginScreen.address.value
            role = loginScreen.role.get_selected_objects()[0];

            if not self.setup(address):
                popup = npyscreen.Popup(name="Login failed")
                popup.add_widget(npyscreen.FixedText
                    , value="Please check the address and try again later"
                    , editable=False)
                popup.edit()
            else:
                break

        # launch main screen
        mainScreen = MainScreen("[" + nickname + " as " + role + "]")
        mainScreen.edit();

    # setup the node
    def setup(self, address):
        if address.split(":")[0] == "127.0.0.1":
            return self.launch();
        else:
            return self.login(address)

    # login to remote server
    def login(self, address):
        return False;

    # launch the node itself
    def launch(self):
        return True

if __name__ == "__main__":
    App = App()
    App.run()

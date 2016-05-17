#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from screens.LoginScreen import LoginScreen
from screens.CreateUserScreen import CreateUserScreen
from screens.MainScreen import MainScreen

class App(npyscreen.NPSApp):
    def main(self):
        loginScreen  = LoginScreen()
        loginScreen.edit();

        createUserScreen = CreateUserScreen()
        createUserScreen.edit();

        mainScreen = MainScreen()
        mainScreen.edit();

if __name__ == "__main__":
    App = App()
    App.run()

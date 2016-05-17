#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from LoginScreen import LoginScreen
from CreateUserScreen import CreateUserScreen
from MainScreen import MainScreen

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

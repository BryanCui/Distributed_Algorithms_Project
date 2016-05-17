#!/usr/bin/env python
# encoding: utf-8

import npyscreen
from GUI.LoginScreen import LoginScreen
from GUI.CreateUserScreen import CreateUserScreen
from GUI.MainScreen import MainScreen

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

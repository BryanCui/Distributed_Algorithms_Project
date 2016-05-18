#!/usr/bin/env python
# encoding: utf-8

import npyscreen

class PeopleList(npyscreen.MultiLineAction):

    def __init__(self, *args, **keywords):
        super(npyscreen.MultiLineAction, self).__init__(*args, **keywords)
    
    def actionHighlighted(self, act_on_this, key_press):
        popup = npyscreen.Popup(
            name=act_on_this
            , columns=20
            ,relx=50)

        popup.add(npyscreen.MultiLineAction
            , name="7 Goods on sale:"
            , values = [
                "Goods 1"
                ,"Goods 2"
                ,"Goods 3"
                ,"Goods 4"
                ,"Goods 5"
                ,"Goods 6"
                ,"Goods 7"
            ]
            , scroll_exit=True)
        popup.edit()

# Copyright 2013 Raihan Kibria
#
# This file is part of Pyco.
#
# Pyco is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyco is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pyco.  If not, see <http://www.gnu.org/licenses/>.

import kivy
kivy.require('1.8.0')

import os
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class ChooseOptionPopup:
    m_dictOptionCallback = None
    
    def __init__(self, title, listOptionCallback):
        self.m_dictOptionCallback = {}
        
        layout = BoxLayout(orientation="vertical")
        
        for option,callback in listOptionCallback:
            if callback != None:
                self.m_dictOptionCallback[option] = callback
                btn = Button(text=option, size_hint=(1, 0.1))
                btn.bind(on_release = self.choice)
                layout.add_widget(btn)
            else:
                layout.add_widget(Label(text=option, size_hint=(1, 0.1)))
        
        self.popup = Popup(title=title,content=layout,size_hint=(0.5, min(0.1 + len(listOptionCallback) * 0.1, 1.0)))
        self.popup.open()
        
    def choice(self, instance):
        self.dismiss_popup()
        (self.m_dictOptionCallback[instance.text])()
        
    def dismiss_popup(self):
        self.popup.dismiss()
 
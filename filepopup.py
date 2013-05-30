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
kivy.require('1.7.0')

import os
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class FilePopup:
    m_fctOpenCallback = None
    
    def __init__(self, open_callback, popuptitle):
        self.m_fctOpenCallback = open_callback
        layout = BoxLayout(orientation="vertical")
        self.selection = TextInput(multiline=False,text=os.getcwd() + os.sep,
            readonly=False,size_hint=(1,0.1),focus=True)
        layout.add_widget(self.selection)
        filechooser = FileChooserListView(filters=["*.py","*.txt"],path=os.getcwd())
        layout.add_widget(filechooser)
        filechooser.bind(selection = self.on_selection)
        buttonslayout = BoxLayout(size_hint=(1, 0.1),orientation="horizontal")
        btn1 = Button(text='OK', size_hint=(0.5, 1))
        btn1.bind(on_release = self.on_ok_button)
        buttonslayout.add_widget(btn1)
        btn2 = Button(text='Cancel', size_hint=(0.5, 1))
        btn2.bind(on_release = self.on_cancel_button)
        buttonslayout.add_widget(btn2)
        layout.add_widget(buttonslayout)
        self.popup = Popup(title=popuptitle,content=layout,size_hint=(1,1))
        self.popup.open()
        
    def on_selection(self, instance, value):
        self.selection.text = value and value[0] or ""

    def on_ok_button(self, instance):
        self.m_fctOpenCallback(self.selection.text)
        self.dismiss_popup()
        
    def on_cancel_button(self, instance):
        self.dismiss_popup()
        
    def dismiss_popup(self):
        self.popup.dismiss()
 

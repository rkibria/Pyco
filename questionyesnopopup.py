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
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

class QuestionYesNoPopup:
    m_fctAnswerCallback = None
    m_bAnswer = None
    
    def __init__(self, popuptitle, popupquestion, answercallback):
        self.m_fctAnswerCallback = answercallback
        
        layout = BoxLayout(orientation="vertical")
        
        layout.add_widget(Label(text=popupquestion))
        
        buttonslayout = BoxLayout(size_hint=(1, 0.2),orientation="horizontal")
        btn1 = Button(text='Yes', size_hint=(0.5, 1))
        btn1.bind(on_release = self.on_yes_button)
        buttonslayout.add_widget(btn1)
        btn2 = Button(text='No', size_hint=(0.5, 1))
        btn2.bind(on_release = self.on_no_button)
        buttonslayout.add_widget(btn2)
        layout.add_widget(buttonslayout)
        
        self.popup = Popup(title=popuptitle,content=layout,size_hint=(0.75, 0.5))
        self.popup.open()
        
    def on_yes_button(self, instance):
        self.m_bAnswer = True
        self.dismiss_popup()
        
    def on_no_button(self, instance):
        self.m_bAnswer = False
        self.dismiss_popup()
        
    def dismiss_popup(self):
        if self.m_fctAnswerCallback:
            self.m_fctAnswerCallback(self.m_bAnswer)
        self.popup.dismiss()
 
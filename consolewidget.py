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

import sys
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.codeinput import CodeInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from cStringIO import StringIO
import kivy.resources

from filepopup import FilePopup

class ConsoleWidget(BoxLayout):
    m_oMainWidget = None
    myglobals = {}
    history = list()
    historyindex = 0
            
    def __init__(self, oMainWidget, **kwargs):
        super(ConsoleWidget, self).__init__(**kwargs)
        self.m_oMainWidget = oMainWidget
        
        self.orientation="vertical"
        
        self.inputlayout = BoxLayout(orientation='vertical', size_hint=(1, 0.1))
        self.make_consoleinput()
        self.add_widget(self.inputlayout)

        buttonslayout = BoxLayout(size_hint=(1, 0.1),orientation="horizontal")
        label1 = Label(text="History:", size_hint=(0.1, 1))
        buttonslayout.add_widget(label1)
        btn1 = Button(text='<', size_hint=(1.0 / 20.0, 1))
        btn1.bind(on_press = self.on_history_back)
        buttonslayout.add_widget(btn1)
        btn2 = Button(text='>', size_hint=(1.0 / 20.0, 1))
        btn2.bind(on_press = self.on_history_forward)
        buttonslayout.add_widget(btn2)
        buttonslayout.add_widget(Label(text="Screen:", size_hint=(0.1, 1)))
        btn3 = Button(text='Clear', size_hint=(0.1, 1))
        btn3.bind(on_press = self.on_clearbutton)
        buttonslayout.add_widget(btn3)
        buttonslayout.add_widget(Label(text="Editor:", size_hint=(0.1, 1)))
        btn4 = Button(text='New', size_hint=(0.1, 1))
        btn4.bind(on_press = self.on_console_new_editor)
        buttonslayout.add_widget(btn4)
        btn5 = Button(text='Open', size_hint=(0.1, 1))
        btn5.bind(on_press = self.on_console_open_editor)
        buttonslayout.add_widget(btn5)
        self.add_widget(buttonslayout)
        
        self.consoleoutput = CodeInput(multiline=True,text="Python "+sys.version+"\n",readonly=True,
            font_name=kivy.resources.resource_find("DroidSansMonoDotted.ttf"))
        self.add_widget(self.consoleoutput)
        
    def prnt(self, txt):
        if len(txt) > 0:
            self.consoleoutput.text += txt
    
    def on_clearbutton(self, instance):
        self.consoleoutput.text = ""
    
    def on_history_back(self, instance):
        if len(self.history) > 0:
            self.consoleinput.text = self.history[self.historyindex]
            if self.historyindex > 0:
                self.historyindex -= 1
        
    def on_history_forward(self, instance):
        if self.historyindex < len(self.history) - 1:
            self.historyindex += 1
            self.consoleinput.text = self.history[self.historyindex]
        
    def add_to_history(self, cmdline):
        if len(self.history) == 0 or self.history[-1] != cmdline:
            self.history.append(cmdline)

    def run_script(self, scripttext):
        try:
            old_stdout = sys.stdout
            redirected_output = sys.stdout = StringIO()
            exec(scripttext, self.myglobals)
            sys.stdout = old_stdout
            return redirected_output.getvalue()
        except Exception, e:
            return "ERROR: " + str(e) + "\n"
        
    def on_command_entered(self, instance):
        cmdline = instance.text
        if cmdline != "":
            self.prnt(">>> " + cmdline + "\n")
            self.add_to_history(cmdline)
            self.prnt(self.run_script(cmdline))
        self.historyindex = len(self.history) - 1
        self.make_consoleinput()
        
    def on_console_new_editor(self, instance):
        self.m_oMainWidget.create_editor_tab()
    
    def on_console_open_editor(self, instance):
        FilePopup(self.on_open_file, "Open")

    def on_open_file(self, filename):
        self.m_oMainWidget.create_editor_tab(filename)
    
    def make_consoleinput(self):
        self.inputlayout.clear_widgets()
        self.consoleinput = CodeInput(multiline=False,focus=True,
            font_name=kivy.resources.resource_find("DroidSansMonoDotted.ttf"))
        self.consoleinput.bind(on_text_validate = self.on_command_entered)
        self.inputlayout.add_widget(self.consoleinput)

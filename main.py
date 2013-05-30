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

from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem

from consolewidget import ConsoleWidget
from editorwidget import EditorWidget

class PythonConsole(TabbedPanel):
    def __init__(self, **kwargs):
        super(PythonConsole, self).__init__(**kwargs)
        
        self.console = ConsoleWidget(self)
        tab1 = TabbedPanelItem(text="Console")
        tab1.add_widget(self.console)
        self.add_widget(tab1)
        
    def remove_tab(self, oTab):
        self.activate_console()
        self.remove_widget(oTab)
    
    def activate_newest_tab(self):
        self.switch_to(self.tab_list[0])
        
    def activate_console(self):
        self.switch_to(self.tab_list[-1])
    
    def create_editor_tab(self, filename = None):
        tab2 = TabbedPanelItem(text="Editor")
        editor = EditorWidget(self, tab2, filename)
        tab2.add_widget(editor)
        self.add_widget(tab2)
        self.activate_newest_tab()
        
    def trace(self, txt):
        self.console.prnt("TRACE: " + txt + "\n")
        
    def run_script(self, scripttext):
        self.activate_console()
        self.console.prnt(self.console.run_script(scripttext))

class PythonConsoleApp(App):
    def build(self):
        return PythonConsole(do_default_tab = False)

if __name__ == '__main__':
    PythonConsoleApp().run()

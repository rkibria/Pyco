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

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import os
import kivy.resources
from kivy.uix.scrollview import ScrollView

from filepopup import FilePopup
from questionyesnopopup import QuestionYesNoPopup

class EditorWidget(BoxLayout):
    m_oMainWidget = None
    m_strFilename = None
    m_oEditorInput = None
    m_bIsModified = False
    m_bIgnoredFirstTextChange = False
    m_oLineLabel = None
    
    def __init__(self, oMainWidget, oParentTab, filename, **kwargs):
        super(EditorWidget, self).__init__(**kwargs)
        self.m_oMainWidget = oMainWidget
        self.m_strFilename = filename
        self.m_oParentTab = oParentTab
                
        self.orientation="vertical"
        
        self.scrollcontainer = BoxLayout(orientation="vertical",size_hint=(1, 0.9))
        self.add_widget(self.scrollcontainer)
        self.textscroll = ScrollView(size_hint=(1,1))
        self.scrollcontainer.add_widget(self.textscroll)
        loadedtext = self.load_file()
        self.m_oEditorInput = TextInput(multiline=True,size_hint_y = None,focus=True,
            auto_indent=True,font_name=kivy.resources.resource_find("DroidSansMonoDotted.ttf"),
            text=loadedtext, height=((loadedtext.count("\n") + 1) * 18 + 640))
        self.m_oEditorInput.bind(text = self.on_text_changed)
        self.textscroll.add_widget(self.m_oEditorInput)

        buttonslayout = BoxLayout(orientation = "horizontal",size_hint=(1, 0.1))

        savebutton = Button(text="Save",size_hint=(0.1, 1))
        buttonslayout.add_widget(savebutton)
        savebutton.bind(on_release = self.on_save_button)
        
        runbutton = Button(text="Run",size_hint=(0.1, 1))
        buttonslayout.add_widget(runbutton)
        runbutton.bind(on_release = self.on_run_button)
        
        closebutton = Button(text="Close",size_hint=(0.1, 1))
        buttonslayout.add_widget(closebutton)
        closebutton.bind(on_release = self.on_close_button)
        
        self.m_oLineLabel = Label(text=self.get_cursor_pos_string(),size_hint=(0.1, 1))
        buttonslayout.add_widget(self.m_oLineLabel)
        self.m_oEditorInput.bind(cursor_pos = self.on_cursor_pos_changed)
        
        self.add_widget(buttonslayout)
        
        self.editorlabel = Label(text=(self.m_strFilename 
            if self.m_strFilename != None else "No file"),size_hint=(1, 0.1))
        self.add_widget(self.editorlabel)
        
        self.m_bIsModified = False
        self.set_tab_name()
        
    def on_cursor_pos_changed(self, instance, value):
        self.m_oLineLabel.text = self.get_cursor_pos_string()
        
    def get_cursor_pos_string(self):
        return "Ln %d Col %d" % (self.m_oEditorInput.cursor_row + 1, self.m_oEditorInput.cursor_col + 1)
    
    def on_close_button(self, instance):
        if self.m_bIsModified:
            self.yesnopopup = QuestionYesNoPopup("Close editor", 
                "You have unsaved changes, really close?", 
                self.close_callback)
        else:
            self.close_callback(True)
    
    def close_callback(self, bAnswer):
        if bAnswer:
            self.m_oMainWidget.remove_tab(self.m_oParentTab)
        
    def on_run_button(self, instance):
        self.m_oMainWidget.run_script(self.m_oEditorInput.text)
    
    def on_save_button(self, instance):
        if self.m_strFilename != None:
            self.write_to_file()
        else:
            self.filepopup = FilePopup(self.on_save_as_file, "Save As")
    
    def write_to_file(self):
        if self.m_strFilename != None:
            with open(self.m_strFilename, 'w') as outfile:
                outfile.write(self.m_oEditorInput.text)
            self.m_bIsModified = False
            self.set_tab_name()
    
    def on_save_as_file(self, filename):
        if os.path.isfile(filename):
            self.overwritefilename = filename
            self.yesnopopup = QuestionYesNoPopup("Save", 
                "Overwrite file %s?" % filename, 
                self.save_overwrite_callback)
        else:
            self.do_write(filename)
    
    def do_write(self, filename):
        self.m_strFilename = filename
        self.editorlabel.text = self.m_strFilename
        self.write_to_file()
    
    def save_overwrite_callback(self, bAnswer):
        if bAnswer:
            self.do_write(self.overwritefilename)
    
    def on_text_changed(self, instance, value):
        if self.m_bIgnoredFirstTextChange == False:
            self.m_bIgnoredFirstTextChange = True
            return
        self.m_bIsModified = True
        self.set_tab_name()
        self.set_edit_size()
    
    def set_edit_size(self):
        self.m_oEditorInput.height = ((self.m_oEditorInput.text.count("\n") + 1) 
            * self.m_oEditorInput.line_height + 640)
    
    def load_file(self):
        loadedtext = ""
        if self.m_strFilename and self.m_strFilename != "":
            with open(self.m_strFilename) as stream:
                loadedtext = stream.read()
        return loadedtext
        
    def set_tab_name(self):
        if self.m_strFilename == None or self.m_strFilename == "":
            tabname = "Editor"
        else:
            basename = os.path.basename(self.m_strFilename)
            tabname = basename if len(basename) <= 10 else basename[0:9] + "..."
        tabname += "*" if self.m_bIsModified else ""
        self.m_oParentTab.text = tabname

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
from kivy.core.clipboard import Clipboard

from filepopup import FilePopup
from questionyesnopopup import QuestionYesNoPopup
from chooseoptionpopup import ChooseOptionPopup

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

        filebutton = Button(text="File",size_hint=(0.1, 1))
        buttonslayout.add_widget(filebutton)
        filebutton.bind(on_release = self.on_file_button)

        editbutton = Button(text="Edit",size_hint=(0.1, 1))
        buttonslayout.add_widget(editbutton)
        editbutton.bind(on_release = self.on_edit_button)

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
    
    def on_file_button(self, instance):
        self.chooseoptionpopup = ChooseOptionPopup("File", 
            [
             ("Save", self.on_save_button), 
             ("Run", self.on_run_button), 
             ("", None),
             ("Close", self.on_close_button),
             ]
             )

    def on_edit_button(self, instance):
        listOptions = list()
        
        bSelection = (self.m_oEditorInput.selection_text != "")
        if bSelection:
            listOptions.append(("Cut", self.on_cut_button))
            listOptions.append(("Copy", self.on_copy_button))
        
        clipboardcontents = None
        try:
            clipboardcontents = Clipboard.get('UTF8_STRING')
        except:
            pass
        if clipboardcontents and len(clipboardcontents) > 0:
            listOptions.append(("Paste", self.on_paste_button))
        
        if bSelection:
            listOptions.append(("", None))
            listOptions.append(("Indent", self.on_indent_button))
            listOptions.append(("Unindent", self.on_unindent_button))
        
        if len(listOptions) > 0:
            self.chooseoptionpopup = ChooseOptionPopup("Edit", listOptions)

    def on_cut_button(self):
        selection = self.m_oEditorInput.selection_text
        if selection != "":
            Clipboard.put(selection, 'UTF8_STRING')
            self.m_oEditorInput.delete_selection()

    def on_copy_button(self):
        selection = self.m_oEditorInput.selection_text
        if selection != "":
            Clipboard.put(selection, 'UTF8_STRING')

    def on_paste_button(self):
        clipboardcontents = Clipboard.get('UTF8_STRING')
        if clipboardcontents and len(clipboardcontents) > 0:
            self.m_oEditorInput.insert_text(clipboardcontents)

    def get_tab_chars(self):
        return "\t"
        
    def on_indent_button(self):
        startindex, endindex = self.get_indent_area()
        
        if startindex != None:
            fulltext = self.m_oEditorInput.text
            source = ""
            
            if startindex == 0:
                source += self.get_tab_chars()
                
            for sourceindex in range(startindex, endindex):
                if sourceindex < len(fulltext):
                    source += fulltext[sourceindex]
            
            indented = ""
            for originalchar in source:
                indented += originalchar
                if originalchar == "\n":
                    indented += self.get_tab_chars()
                    
            self.m_oEditorInput.select_text(startindex, endindex)
            
            self.m_oEditorInput.delete_selection()
            self.m_oEditorInput.insert_text(indented)
            self.m_oEditorInput.select_text(startindex, startindex + len(indented))
            
    def get_indent_area(self):
        selection = self.m_oEditorInput.selection_text
        if selection and len(selection) > 0:
            selection_from = self.m_oEditorInput.selection_from
            selection_to = self.m_oEditorInput.selection_to
            
            if selection_from > selection_to:
                temp = selection_from
                selection_from = selection_to
                selection_to = temp
            
            fulltext = self.m_oEditorInput.text
            
            # Find place where to start indenting
            startindex = selection_from
            while (startindex >= 0):
                if startindex < len(fulltext):
                    character = fulltext[startindex]
                    if character == "\n":
                        break
                    else:
                        startindex -= 1
                
            if startindex <= 0:
                startindex = 0
                
            endindex = selection_to
            return (startindex, endindex)
        else:
            return (None, None)
    
    def on_unindent_button(self):
        startindex, endindex = self.get_indent_area()
        
        if startindex != None:
            self.m_oEditorInput.select_text(startindex, endindex)
            selection = self.m_oEditorInput.selection_text
            
            # Delete one indentation level from every line
            unindented = ""
            bDoneLine = False
            for character in selection:
                if character == self.get_tab_chars():
                    if bDoneLine:
                        unindented += character
                    else:
                        bDoneLine = True
                elif character == "\n":
                    unindented += character
                    bDoneLine = False
                else:
                    unindented += character
            
            self.m_oEditorInput.delete_selection()
            self.m_oEditorInput.insert_text(unindented)
            self.m_oEditorInput.select_text(startindex, startindex + len(unindented))

    def on_close_button(self):
        if self.m_bIsModified:
            self.yesnopopup = QuestionYesNoPopup("Close editor", 
                "You have unsaved changes, really close?", 
                self.close_callback)
        else:
            self.close_callback(True)
    
    def close_callback(self, bAnswer):
        if bAnswer:
            self.m_oMainWidget.remove_tab(self.m_oParentTab)
        
    def on_run_button(self):
        self.m_oMainWidget.run_script(self.m_oEditorInput.text)
    
    def on_save_button(self):
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

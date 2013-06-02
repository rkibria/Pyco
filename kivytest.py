from kivy.app import App
from kivy.uix.button import Button

class TestApp(App):
    def build(self):
        button = Button(text='Hello World')
        button.bind(on_press = self.on_press)
        return button
        
    def on_press(self, instance):
        self.stop()
 
TestApp().run()

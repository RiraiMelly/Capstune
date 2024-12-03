from kivy.uix.screenmanager import Screen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')

        label = MDLabel(text='About Screen', halign='center')
        layout.add_widget(label)

        self.add_widget(layout)

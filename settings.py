from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = MDBoxLayout(orientation='vertical')
        label = MDLabel(text='Settings Screen', halign='center')

        # Button to toggle theme
        toggle_button = MDRaisedButton(text='Toggle Dark/Light Mode', on_release=self.toggle_theme)

        layout.add_widget(label)
        layout.add_widget(toggle_button)
        self.add_widget(layout)

    def toggle_theme(self, instance):
        # Call the toggle_theme method from the main app
        app = MDApp.get_running_app()
        app.toggle_theme()

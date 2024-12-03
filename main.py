from kivy.config import Config
Config.set('graphics', 'stencilbuffer', '0')
Config.set('graphics', 'multisamples', '0')
Config.set('graphics', 'gl_backend', 'angle_sdl2')
Config.set('graphics', 'width', '380')
Config.set('graphics', 'height', '640')
from kivymd.icon_definitions import md_icons  
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.lang import Builder
import subprocess
import os
import sys

KV = '''
Screen:
    MDBottomNavigation:
        MDBottomNavigationItem:
            name: 'home'
            text: 'Home'
            icon: 'home'
            
            MDLabel:
                text: "Main"
                halign: 'center'

        MDBottomNavigationItem:
            name: 'settings'
            text: 'Settings'
            icon: 'cog'
            
            MDLabel:
                text: "Main"
                halign: 'center'

        MDBottomNavigationItem:
            name: 'about'
            text: 'About'
            icon: 'information'
        
            MDLabel:
                text: "Main"
                halign: 'center'
'''

class MainApp(MDApp):
    def build(self):
        # Set the initial background color to dark gray
        sm = ScreenManager(transition=NoTransition())
        Window.clearcolor = (0.1, 0.1, 0.1, 1)  # RGBA
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_file('main.kv')

    def toggle_theme(self, switch_instance, value):
        if value:
            self.theme_cls.theme_style = "Light"
            Window.clearcolor = (1, 1, 1, 1)  # White background for light mode
        else:
            self.theme_cls.theme_style = "Dark"
            Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark gray background for dark mode

    def _run_script(self, script_name):
        """Helper function to run a Python script."""
        if sys.platform == 'win32':
            venv_python = os.path.join(sys.prefix, 'Scripts', 'python.exe')
        else:
            venv_python = os.path.join(sys.prefix, 'bin', 'python')

        script_path = os.path.join(os.path.dirname(__file__), script_name)
        script_path = os.path.abspath(script_path)

        if not os.path.isfile(script_path):
            print(f"{script_name} not found: {script_path}")
            return  # Exit if the script doesn't exist
        
        try:
            cwd = os.path.dirname(script_path)
            subprocess.Popen([venv_python, script_path], cwd=cwd)
            print(f"Launched {script_name} successfully.")
        except Exception as e:
            print(f"Error launching {script_name}: {e}")

    def run_open_cv(self):
        self._run_script('open_cv.py')

    def run_inference_classifier(self):
        self._run_script('inference_classifier.py')

    def run_inference_classifier_letter(self):
        self._run_script('inference_letters.py')

    # LMS Methods
    def run_lms_login(self):
        self._run_script('lms_login.py')

    def run_lms_dashboard(self):
        self._run_script('lms_dashboard.py')

    def run_lms_course(self):
        self._run_script('lms_course.py')
        
class BottomNav(FloatLayout):
    pass

if __name__ == "__main__":
    MainApp().run()

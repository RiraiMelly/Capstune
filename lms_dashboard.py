from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.uix.list import OneLineListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton

class LMSDashboard(Screen):
    def __init__(self, lms_db, **kwargs):
        super().__init__(**kwargs)
        self.lms_db = lms_db
        self.build_dashboard()

    def build_dashboard(self):
        # Scrollable container for courses
        scroll_view = ScrollView()
        self.courses_list = MDBoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
        self.courses_list.bind(minimum_height=self.courses_list.setter('height'))
        scroll_view.add_widget(self.courses_list)
        self.add_widget(scroll_view)

        # Fetch courses from the database and add them to the list
        self.load_courses()

        # Add a back button to return to the main screen

    def load_courses(self):
        self.courses_list.clear_widgets()
        courses = self.lms_db.get_courses()
        for course_id, title in courses:
            item = OneLineListItem(
                text=title,
                on_press=lambda x, cid=course_id: print(f"Selected Course ID: {cid}")
            )
            self.courses_list.add_widget(item)

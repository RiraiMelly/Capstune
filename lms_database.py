import sqlite3
import os

class LMSDatabase:
    def __init__(self, db_name="lms_data.db"):
        self.db_path = os.path.join(os.path.dirname(__file__), db_name)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Create users and courses tables
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                course_id INTEGER,
                progress INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (course_id) REFERENCES courses (id)
            )
        ''')

        self.connection.commit()

    def add_user(self, username, password):
        try:
            self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_course(self, title, description):
        self.cursor.execute('INSERT INTO courses (title, description) VALUES (?, ?)', (title, description))
        self.connection.commit()

    def get_courses(self):
        self.cursor.execute('SELECT id, title FROM courses')
        return self.cursor.fetchall()

    def track_progress(self, user_id, course_id, progress):
        self.cursor.execute('''
            INSERT OR REPLACE INTO progress (user_id, course_id, progress)
            VALUES (?, ?, ?)
        ''', (user_id, course_id, progress))
        self.connection.commit()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    # Initialize and populate the database for testing
    db = LMSDatabase()
    db.add_course("Python Basics", "Learn the fundamentals of Python programming.")
    db.add_course("Advanced Kivy", "Build modern UIs with Kivy and KivyMD.")
    print("Courses:", db.get_courses())
    db.close()

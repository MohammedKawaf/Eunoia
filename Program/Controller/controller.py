import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Model.read_db import Read_db
from Model.write_db import Write_db
from View.login import LoginView
from View.main_window import MainWindow
from View.sign_up import SignUpView
import tkinter as tk

class Controller:
    def __init__(self):
        self.read_db = Read_db()
        self.write_db = Write_db()
        self.current_user = None
        self.current_mood = None
        
        # Skapa endast en Tk-instans
        self.root = tk.Tk()
        self.root.withdraw()  # Göm huvudfönstret
        
        # Färger och typsnitt som kan användas av alla vyer
        self.COLORS = {
            'primary': "#4A90E2",      # Modern blue
            'secondary': "#357ABD",    # Darker blue
            'accent': "#F5F9FF",       # Light blue
            'background': "#FFFFFF",    # Pure white
            'text': "#2C3E50",         # Modern dark blue-gray
            'light_gray': "#F8F9FA",   # Lighter gray
            'success': "#27AE60",      # Green
            'warning': "#E74C3C",      # Red
            'gradient_start': "#4A90E2",  # Start of gradient
            'gradient_end': "#357ABD",    # End of gradient
            'card_shadow': "#E1E8ED",   # Shadow color
            'hover': "#EDF2F7"         # Hover state color
        }
        
        self.FONTS = {
            'title': ('Segoe UI', 48, 'bold'),
            'heading': ('Segoe UI', 24, 'bold'),
            'subheading': ('Segoe UI', 16, 'normal'),
            'body': ('Segoe UI', 12, 'normal'),
            'button': ('Segoe UI', 12, 'bold'),
            'small': ('Segoe UI', 10, 'normal')
        }
        
        # Definiera mood recommendations
        self.mood_recommendations = {
            1: [
                "Take a gentle walk in nature",
                "Practice deep breathing exercises for 5 minutes",
                "Reach out to a friend or family member",
                "Try some light stretching or yoga",
                "Write down three things you're grateful for"
            ],
            2: [
                "Listen to uplifting music",
                "Do a 10-minute meditation session",
                "Take a warm, relaxing bath",
                "Write down your feelings",
                "Plan a fun activity for tomorrow"
            ],
            3: [
                "Try a new hobby or activity",
                "Organize your space",
                "Take a short walk during lunch",
                "Practice mindfulness",
                "Connect with a friend"
            ],
            4: [
                "Share your positive energy with others",
                "Start a new project you're excited about",
                "Try a challenging workout",
                "Learn something new",
                "Help someone in need"
            ],
            5: [
                "Set new goals for yourself",
                "Try teaching someone a skill",
                "Take on a leadership role",
                "Start a gratitude journal",
                "Plan a future adventure"
            ]
        }

        # Initiera vyer
        self.login_view = None
        self.main_window = None
        self.sign_up_view = None

    def start(self):
        if not self.login_view:
            self.login_view = LoginView(self)
        self.login_view.show()

    def save_todo(self, task):
        if self.current_user and task:
            self.write_db.add_todo(self.current_user, task)
            return True
        return False

    def get_todos(self):
        if self.current_user:
            todos = self.read_db.get_todos(self.current_user)
            if todos:
                # Konvertera från dictionary till lista om det behövs
                if isinstance(todos, dict):
                    return [value for value in todos.values()]
                return todos
        return []

    def delete_todo(self, todo):
        if self.current_user:
            self.write_db.delete_todo(self.current_user, todo)


    def toggle_todo(self, todo):
        if self.current_user:
            self.write_db.toggle_todo(self.current_user, todo)

    def set_current_mood(self, mood):
        self.current_mood = int(float(mood))
        # Ta bort gamla rekommendationer innan vi lägger till nya
        self.write_db.remove_old_recommendations(self.current_user)
        # Spara endast dagens rekommendationer
        recommendations = self.get_mood_recommendations()
        self.write_db.add_mood_recommendations(self.current_user, recommendations, self.current_mood)

    def get_mood_recommendations(self):
        if self.current_mood is None:
            return []
        return self.mood_recommendations.get(self.current_mood, [])

    def get_mood_description(self, mood):
        descriptions = {
            1: "Very Low - Need extra care today",
            2: "Low - Could use some uplift",
            3: "Neutral - Balanced",
            4: "Good - Positive energy",
            5: "Excellent - Feeling great!"
        }
        return descriptions.get(int(float(mood)), "Neutral - Balanced")

    def show_main_window(self):
        if not self.main_window:
            self.main_window = MainWindow(self)
        self.main_window.show()
        self.login_view.hide()

    def show_sign_up(self):
        if not self.sign_up_view:
            self.sign_up_view = SignUpView(self)
        self.sign_up_view.show()
        self.login_view.hide()

    def show_login(self):
        if self.sign_up_view:
            self.sign_up_view.hide()
        if self.main_window:
            self.main_window.hide()
        self.login_view.show()

    def login(self, username, password):
        users = self.read_db.get_users()
        if username in users and users[username]["password"] == password:
            self.current_user = username
            return True
        return False

    def register(self, username, password):
        users = self.read_db.get_users()
        if username and password:
            if username not in users:
                self.write_db.add_user(username, password)
                return True
        return False    

    def logout(self):
        self.current_user = None
        self.current_mood = None
        if self.main_window:
            self.main_window.root.destroy()  # Stäng huvudfönstret helt
            self.main_window = None  # Ta bort referensen
        if self.login_view:
            self.login_view.clear_entries()  # Rensa inloggningsfälten
            self.login_view.show()  # Visa inloggningsfönstret igen

    def adjust_color(self, color, amount):
        def clamp(x): return max(0, min(x, 255))
        if len(color) != 7: return color
        r = clamp(int(color[1:3], 16) + amount)
        g = clamp(int(color[3:5], 16) + amount)
        b = clamp(int(color[5:7], 16) + amount)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    # Closes the entire application
    def quit(self):
        self.root.quit()
        self.root.destroy()
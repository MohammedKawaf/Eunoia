import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase

from datetime import datetime

class Write_db:
    def __init__(self):
        config = {
            "apiKey": "AIzaSyAmM99rqwou4T1TM_z214G6DaitgazPpo8",
            "authDomain": "eunoia-4a32f.firebaseapp.com",
            "databaseURL": "https://eunoia-4a32f-default-rtdb.europe-west1.firebasedatabase.app/",
            "projectId": "eunoia-4a32f",
            "storageBucket": "eunoia-4a32f.firebasestorage.app",
            "messagingSenderId": "653346616435",
            "appId": "1:653346616435:web:3f2f676f7136fd287de606",
            "measurementId": "G-HXDPRH4W7Y"
        }
        firebase = pyrebase.initialize_app(config)
        self.database = firebase.database()
        
    def add_user(self, username, password):
        self.database.child("users").child(username).set({"password": password})
        
    def add_todo(self, username, task):
        new_todo = {
            'task': task,
            'done': False,
            'created_at': datetime.now().isoformat()
        }
        self.database.child("todos").child(username).push(new_todo)
        
    def add_journal(self, username, text):
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_journal = {
            'text': text,
            'mood': '3'
        }
        self.database.child("journals").child(username).child(current_date).set(new_journal)

    def delete_todo(self, username, todo):
        todos = self.database.child("todos").child(username).get()
        if todos.val():
            for key, value in todos.val().items():
                if value == todo:
                    self.database.child("todos").child(username).child(key).remove()
            
    def delete_journal(self, username, date):
        self.database.child("journals").child(username).child(date).remove()
        
    def toggle_todo(self, username, todo):
        if 'key' in todo:
            self.database.child("todos").child(username).child(todo['key']).update({
                'done': todo['done']
            })
        
    def add_mood_recommendations(self, username, recommendations, mood):
        for rec in recommendations:
            new_task = {
                'task': rec,
                'done': False,
                'created_at': datetime.now().isoformat(),
                'is_recommendation': True,
                'mood_level': mood
            }
            self.database.child("todos").child(username).push(new_task)
        
    def remove_old_recommendations(self, username):
        todos = self.database.child("todos").child(username).get()
        if todos.val():
            for key, value in todos.val().items():
                if value.get('is_recommendation'):
                    self.database.child("todos").child(username).child(key).remove()
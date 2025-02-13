import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pyrebase

class Read_db:
    def __init__(self):
        config = {  
            "apiKey": "AIzaSyAmM99rqwou4T1TM_z214G6DaitgazPpo8",
            "authDomain": "eunoia-4a32f.firebaseapp.com",
            "databaseURL": "https://eunoia-4a32f-default-rtdb.europe-west1.firebasedatabase.app",
            "projectId": "eunoia-4a32f",
            "storageBucket": "eunoia-4a32f.firebasestorage.app",
            "messagingSenderId": "653346616435",
            "appId": "1:653346616435:web:3f2f676f7136fd287de606",
            "measurementId": "G-HXDPRH4W7Y"}
        firebase = pyrebase.initialize_app(config)
        self.auth = firebase.auth()
        self.database = firebase.database()

    def get_users(self):
        users = self.database.child("users").get()
        if users.val():
            return users.val()
        return {}

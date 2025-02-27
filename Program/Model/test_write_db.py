import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from write_db import Write_db

class TestWriteDB(unittest.TestCase):
    
    @patch("write_db.pyrebase")
    def setUp(self, mock_pyrebase):
        self.mock_pyrebase = mock_pyrebase
        self.mock_firebase = mock_pyrebase.initialize_app.return_value
        self.mock_database = self.mock_firebase.database.return_value
        self.write_db = Write_db()
        
    def test_add_user(self):
        username = "testuser"
        password = "testpass"
        self.write_db.add_user(username, password)
        self.mock_database.child.assert_called_with("users")
        self.mock_database.child().child.assert_called_with(username)
        self.mock_database.child().child().set.assert_called_with({"password": password})
        
    def test_add_todo(self):
        username = "testuser"
        task = "test task"
        with patch('write_db.datetime') as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = "2024-03-14T12:00:00"
            self.write_db.add_todo(username, task)
            
            expected_todo = {
                'task': task,
                'done': False,
                'created_at': "2024-03-14T12:00:00"
            }
            self.mock_database.child.assert_called_with("todos")
            self.mock_database.child().child.assert_called_with(username)
            self.mock_database.child().child().push.assert_called_with(expected_todo)
            
    def test_add_journal(self):
        username = "testuser"
        text = "test journal entry"
        with patch('write_db.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-03-14 12:00:00"
            self.write_db.add_journal(username, text)
            
            expected_journal = {
                'text': text,
                'mood': '3'
            }
            self.mock_database.child().child().child().set.assert_called_with(expected_journal)
            
    def test_delete_todo(self):
        username = "testuser"
        todo = {"task": "test task", "done": False}
        mock_todos = {
            "key1": todo,
            "key2": {"task": "other task", "done": False}
        }
        
        self.mock_database.child().child().get.return_value.val.return_value = mock_todos
        self.write_db.delete_todo(username, todo)
        
        self.mock_database.child().child().child().remove.assert_called_once()
        
    def test_delete_journal(self):
        username = "testuser"
        date = "2024-03-14 12:00:00"
        self.write_db.delete_journal(username, date)
        self.mock_database.child().child().child().remove.assert_called_once()
        
    def test_toggle_todo(self):
        username = "testuser"
        todo = {
            "task": "test task",
            "created_at": "2024-03-14T12:00:00",
            "done": False
        }
        mock_todos = {
            "key1": todo.copy()
        }
        
        self.mock_database.child().child().get.return_value.val.return_value = mock_todos
        self.write_db.toggle_todo(username, todo)
        
        self.mock_database.child().child().child().update.assert_called_with({'done': True})
        
    def test_add_mood_recommendations(self):
        username = "testuser"
        recommendations = ["Exercise", "Meditate"]
        mood = 5
        
        with patch('write_db.datetime') as mock_datetime:
            mock_datetime.now.return_value.isoformat.return_value = "2024-03-14T12:00:00"
            self.write_db.add_mood_recommendations(username, recommendations, mood)
            
            expected_calls = [
                unittest.mock.call({
                    'task': rec,
                    'done': False,
                    'created_at': "2024-03-14T12:00:00",
                    'is_recommendation': True,
                    'mood_level': mood
                }) for rec in recommendations
            ]
            
            self.mock_database.child().child().push.assert_has_calls(expected_calls)
            
    def test_remove_old_recommendations(self):
        username = "testuser"
        mock_todos = {
            "key1": {"task": "task1", "is_recommendation": True},
            "key2": {"task": "task2", "is_recommendation": False},
            "key3": {"task": "task3", "is_recommendation": True}
        }
        
        self.mock_database.child().child().get.return_value.val.return_value = mock_todos
        self.write_db.remove_old_recommendations(username)
        
        # Should be called twice for the two recommendations
        self.assertEqual(self.mock_database.child().child().child().remove.call_count, 2)

if __name__ == '__main__':
    unittest.main() 
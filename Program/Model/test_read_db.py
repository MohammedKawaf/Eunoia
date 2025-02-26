import unittest
from unittest.mock import patch
from read_db import Read_db

class TestReadDB(unittest.TestCase):
    
    @patch("read_db.pyrebase")
    def setUp(self, mock_pyrebase):
        self.mock_pyrebase = mock_pyrebase
        self.mock_firebase = mock_pyrebase.initialize_app.return_value
        self.mock_database = self.mock_firebase.database.return_value
        self.read_db = Read_db()

    def test_get_users_returns_empty_dict_if_no_data(self):
        self.mock_database.child.return_value.get.return_value.val.return_value = None
        result = self.read_db.get_users()
        self.assertEqual(result, {})

    def test_get_todos_returns_data(self):
        mock_todos = ["Go for a ride", "Go to the gym", "Read for 10 minutes"]
        self.mock_database.child.return_value.child.return_value.get.return_value.val.return_value = mock_todos

        result = self.read_db.get_todos("User1")
        self.assertEqual(result, mock_todos)

    def test_get_todos_username_empty_list_if_no_todos(self):
        self.mock_database.child.return_value.child.return_value.get.return_value.val.return_value = None
        
        result = self.read_db.get_todos("user1")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
         

import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Program.View.login import LoginView

class TestLoginView(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.mock_controller = MagicMock()
        self.mock_controller.COLORS = {
            'background': '#FFFFFF',
            'primary': '#007BFF',
            'text': '#000000',
            'light_gray': '#CCCCCC'
        }
        self.mock_controller.FONTS = {
            'title': ('Arial', 24, 'bold'),
            'heading': ('Arial', 18, 'bold'),
            'subheading': ('Arial', 12),
            'body': ('Arial', 10),
            'button': ('Arial', 10, 'bold'),
            'small': ('Arial', 8)
        }
        self.login_view = LoginView(self.mock_controller)

    def tearDown(self):
        self.login_view.root.destroy()
        self.root.destroy()

    def test_initial_state(self):
        self.assertEqual(self.login_view.username_entry.get(), "Email Address")
        self.assertEqual(self.login_view.password_entry.get(), "Password")

    def test_clear_entries(self):
        self.login_view.username_entry.delete(0, 'end')
        self.login_view.username_entry.insert(0, "test@test.com")
        self.login_view.password_entry.delete(0, 'end')
        self.login_view.password_entry.insert(0, "password123")
        
        self.login_view.clear_entries()
        
        self.assertEqual(self.login_view.username_entry.get(), "Email Address")
        self.assertEqual(self.login_view.password_entry.get(), "Password")

    def test_entry_focus_in(self):
        self.login_view.on_entry_focus_in(self.login_view.username_entry, "Email Address")
        self.assertEqual(self.login_view.username_entry.get(), "")

    def test_entry_focus_out(self):
        self.login_view.on_entry_focus_out(self.login_view.username_entry, "Email Address")
        self.assertEqual(self.login_view.username_entry.get(), "Email Address")

    def test_login_empty_fields(self):
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.login_view.login()
            mock_error.assert_called_with("Error", "Please fill in all fields")

    def test_login_success(self):
        self.login_view.username_entry.delete(0, 'end')
        self.login_view.username_entry.insert(0, "test@test.com")
        self.login_view.password_entry.delete(0, 'end')
        self.login_view.password_entry.insert(0, "password123")
        
        self.mock_controller.login.return_value = True
        
        self.login_view.login()
        
        self.mock_controller.login.assert_called_with("test@test.com", "password123")
        self.mock_controller.show_main_window.assert_called_once()

    def test_login_failure(self):
        self.login_view.username_entry.delete(0, 'end')
        self.login_view.username_entry.insert(0, "test@test.com")
        self.login_view.password_entry.delete(0, 'end')
        self.login_view.password_entry.insert(0, "wrongpassword")
        
        self.mock_controller.login.return_value = False
        
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.login_view.login()
            mock_error.assert_called_with("Error", "Invalid email or password")

    def test_show_hide(self):
        self.login_view.show()
        self.assertEqual(self.login_view.root.state(), 'normal')
        self.login_view.hide()
        self.assertEqual(self.login_view.root.state(), 'withdrawn')

    def test_window_title(self):
        self.assertEqual(self.login_view.root.title(), "EUNOIA - We Care")

    def test_on_close(self):
        self.login_view.on_close()
        self.mock_controller.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
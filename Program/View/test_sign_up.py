import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import tkinter as tk

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Program.View.sign_up import SignUpView

class TestSignUpView(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.mock_controller = MagicMock()
        self.mock_controller.COLORS = {
            'background': '#FFFFFF',
            'primary': '#007BFF',
            'text': '#000000',
            'light_gray': '#CCCCCC',
            'card_shadow': '#E0E0E0'
        }
        self.mock_controller.FONTS = {
            'title': ('Arial', 24, 'bold'),
            'heading': ('Arial', 18, 'bold'),
            'subheading': ('Arial', 12),
            'body': ('Arial', 10),
            'button': ('Arial', 10, 'bold'),
            'small': ('Arial', 8)
        }
        self.mock_controller.adjust_color = MagicMock(return_value="#0056b3")
        self.mock_controller.show_login = MagicMock()
        self.mock_controller.register = MagicMock()
        self.sign_up_view = SignUpView(self.mock_controller)
        self.sign_up_view.root = tk.Toplevel()
        self.sign_up_view.root.title("EUNOIA - Register")
        self.sign_up_view.root.minsize(900, 600)

    def tearDown(self):
        if self.sign_up_view.root:
            self.sign_up_view.root.destroy()
        self.root.destroy()

    def test_initial_state(self):
        self.assertEqual(self.sign_up_view.username_entry.get(), "Username")
        self.assertEqual(self.sign_up_view.password_entry.get(), "Password")

    def test_window_properties(self):
        self.root.update()
        self.assertEqual(self.sign_up_view.root.title(), "EUNOIA - Register")
        self.assertTrue(self.sign_up_view.root.resizable()[0])
        self.assertTrue(self.sign_up_view.root.resizable()[1])
        minsize = self.sign_up_view.root.minsize()
        self.assertEqual(minsize, (900, 600))

    def test_entry_focus_in_username(self):
        self.sign_up_view.on_entry_focus_in(self.sign_up_view.username_entry, "Username")
        self.assertEqual(self.sign_up_view.username_entry.get(), "")
        self.assertEqual(self.sign_up_view.username_entry.cget("fg"), self.mock_controller.COLORS['text'])

    def test_entry_focus_in_password(self):
        self.sign_up_view.on_entry_focus_in(self.sign_up_view.password_entry, "Password")
        self.assertEqual(self.sign_up_view.password_entry.get(), "")
        self.assertEqual(self.sign_up_view.password_entry.cget("show"), "●")

    def test_entry_focus_out_username(self):
        self.sign_up_view.username_entry.delete(0, 'end')
        self.sign_up_view.on_entry_focus_out(self.sign_up_view.username_entry, "Username")
        self.assertEqual(self.sign_up_view.username_entry.get(), "Username")
        self.assertEqual(self.sign_up_view.username_entry.cget("fg"), "gray")

    def test_entry_focus_out_password(self):
        self.sign_up_view.password_entry.delete(0, 'end')
        self.sign_up_view.on_entry_focus_out(self.sign_up_view.password_entry, "Password")
        self.assertEqual(self.sign_up_view.password_entry.get(), "Password")
        self.assertEqual(self.sign_up_view.password_entry.cget("show"), "")

    def test_modern_entry_creation(self):
        frame, entry = self.sign_up_view.create_modern_entry(self.sign_up_view.root, "Test")
        self.assertEqual(entry.get(), "Test")
        self.assertEqual(entry.cget("relief"), "flat")
        self.assertEqual(entry.cget("width"), 30)
        self.assertEqual(frame.cget("bg"), self.mock_controller.COLORS['card_shadow'])

    def test_modern_button_creation(self):
        test_command = MagicMock()
        btn_frame = self.sign_up_view.create_modern_button(self.sign_up_view.root, "Test", test_command)
        button = btn_frame.winfo_children()[0]
        self.assertEqual(button.cget("text"), "Test")
        self.assertEqual(button.cget("relief"), "flat")
        self.assertEqual(button.cget("cursor"), "hand2")
        self.assertEqual(button.cget("bg"), self.mock_controller.COLORS['primary'])

    def test_register_empty_fields(self):
        self.sign_up_view.username_entry.delete(0, 'end')
        self.sign_up_view.username_entry.insert(0, "Username")
        self.sign_up_view.password_entry.delete(0, 'end')
        self.sign_up_view.password_entry.insert(0, "Password")

        with patch('tkinter.messagebox.showerror') as mock_error:
            self.sign_up_view.register()
            mock_error.assert_called_with("Error", "Please fill in all fields")

    def test_register_success(self):
        self.sign_up_view.username_entry.delete(0, 'end')
        self.sign_up_view.username_entry.insert(0, "testuser")
        self.sign_up_view.password_entry.delete(0, 'end')
        self.sign_up_view.password_entry.insert(0, "password123")

        self.mock_controller.register.return_value = True
        
        with patch('tkinter.messagebox.showinfo') as mock_info:
            self.sign_up_view.register()
            mock_info.assert_called_once_with("Success", "Registration successful!")
            self.mock_controller.show_login.assert_called_once()

    def test_register_failure(self):
        self.sign_up_view.username_entry.delete(0, 'end')
        self.sign_up_view.username_entry.insert(0, "existinguser")
        self.sign_up_view.password_entry.delete(0, 'end')
        self.sign_up_view.password_entry.insert(0, "password123")

        self.mock_controller.register.return_value = False
        
        with patch('tkinter.messagebox.showerror') as mock_error:
            self.sign_up_view.register()
            mock_error.assert_called_with("Error", "Username already exists")

    def test_show_hide(self):
        self.sign_up_view.show()
        self.assertEqual(self.sign_up_view.root.state(), 'normal')
        self.sign_up_view.hide()
        self.assertEqual(self.sign_up_view.root.state(), 'withdrawn')

if __name__ == '__main__':
    unittest.main()

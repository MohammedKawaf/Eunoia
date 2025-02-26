import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from main_window import MainWindow

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.mock_controller = MagicMock()
        self.mock_controller.COLORS = {
            'background': '#FFFFFF',
            'primary': '#4A90E2',
            'text': '#000000',
            'light_gray': '#F5F5F5',
        }
        self.mock_controller.FONTS = {
            'heading': ('Arial', 24, 'bold'),
            'subheading': ('Arial', 18, 'normal'),
            'body': ('Arial', 12, 'normal'),
            'button': ('Arial', 12, 'bold'),
            'small': ('Arial', 10, 'normal')
        }
        self.window = MainWindow(self.mock_controller)

    def tearDown(self):
        self.window.root.destroy()
        self.root.destroy()

    def test_init(self):
        self.assertEqual(self.window.root.title(), "EUNOIA - We Care")
        self.assertEqual(self.window.controller, self.mock_controller)

    def test_create_menu_button(self):
        test_frame = tk.Frame(self.window.root)
        button = self.window.create_menu_button(test_frame, "Test Button", lambda: None)
        self.assertIsInstance(button, tk.Button)
        self.assertEqual(button.cget("text"), "Test Button")

    def test_update_mood_description(self):
        self.window.show_mood_assessment()
        self.window.update_mood_description("1")
        self.assertEqual(
            self.window.mood_description.cget("text"),
            "Very Low - Need extra care today"
        )
        self.window.update_mood_description("5")
        self.assertEqual(
            self.window.mood_description.cget("text"),
            "Excellent - Feeling great!"
        )

    def test_add_todo(self):
        self.window.show_todo_content()
        self.window.task_entry.insert(0, "Test task")
        self.window.add_todo()
        self.mock_controller.save_todo.assert_called_once_with("Test task")

    @patch('tkinter.messagebox.askyesno')
    def test_delete_todo(self, mock_askyesno):
        mock_askyesno.return_value = True
        test_todo = {"task": "Test task", "done": False}
        
        self.window.show_todo_content()
        
        self.window.delete_todo(test_todo)
        self.mock_controller.delete_todo.assert_called_once_with(test_todo)

    def test_save_journal_empty(self):
        self.window.show_journal_content()
        with patch('tkinter.messagebox.showwarning') as mock_warning:
            self.window.save_journal()
            mock_warning.assert_called_once()
            self.mock_controller.save_journal.assert_not_called()

    def test_create_modern_button(self):
        test_frame = tk.Frame(self.window.root)
        button_frame = self.window.create_modern_button(test_frame, "Test Button", lambda: None)
        button = button_frame.winfo_children()[0]
        self.assertIsInstance(button, tk.Button)
        self.assertEqual(button.cget("text"), "Test Button")
        self.assertEqual(button.cget("bg"), self.mock_controller.COLORS['primary'])

    @patch('tkinter.messagebox.showinfo')
    def test_save_journal_success(self, mock_showinfo):
        self.window.show_journal_content()
        self.window.journal_text.insert('1.0', "Test journal entry")
        self.mock_controller.save_journal.return_value = True
        self.window.save_journal()
        self.mock_controller.save_journal.assert_called_once_with("Test journal entry")
        mock_showinfo.assert_called_once()

    def test_show_journal_entries(self):
        test_journals = {
            "2024-01-01": {"text": "Test entry 1"},
            "2024-01-02": {"text": "Test entry 2"}
        }
        self.mock_controller.get_journals.return_value = test_journals
        self.window.show_journal_entries()
        entries = [widget for widget in self.window.content_frame.winfo_children()[0].winfo_children() 
                  if isinstance(widget, tk.Frame)]
        self.assertGreater(len(entries), 0)

    @patch('tkinter.messagebox.askyesno')
    def test_delete_journal_entry(self, mock_askyesno):
        mock_askyesno.return_value = True
        test_date = "2024-01-01"
        self.window.delete_journal_entry(test_date)
        self.mock_controller.delete_journal.assert_called_once_with(test_date)

    def test_show_todo_content_with_mood(self):
        mood_value = "4"
        self.window.show_todo_content(mood_value)
        self.mock_controller.set_current_mood.assert_called_once_with(mood_value)
        self.mock_controller.get_mood_recommendations.assert_called_once()

    def test_update_todos_list(self):
        test_todos = [
            {"task": "Test task 1", "done": False},
            {"task": "Test task 2", "done": True}
        ]
        self.mock_controller.get_todos.return_value = test_todos
        self.window.show_todo_content()
        self.window.update_todos_list()
        todo_items = self.window.todos_frame.winfo_children()
        self.assertEqual(len(todo_items), len(test_todos))

    def test_show_mood_assessment(self):
        self.window.show_mood_assessment()
        mood_frame = self.window.content_frame.winfo_children()[0]
        elements = mood_frame.winfo_children()
        self.assertTrue(any(isinstance(w, tk.Scale) for w in elements))
        self.assertTrue(any(isinstance(w, tk.Label) and w.cget("text") == "How are you feeling today?" 
                          for w in elements))

if __name__ == '__main__':
    unittest.main()
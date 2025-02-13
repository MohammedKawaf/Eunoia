import tkinter as tk

class MainWindow:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Toplevel()
        self.root.title("EUNOIA - We Care")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.minsize(900, 600)
        
        # Configure root background
        self.root.configure(bg=self.controller.COLORS['background'])
        
        # Main container
        self.main_frame = tk.Frame(self.root, bg=self.controller.COLORS['background'])
        self.main_frame.pack(fill='both', expand=True)
        
        # Content frame for switching between views
        self.content_frame = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create menu
        #self.create_menu() should then be here
        
        # Create content frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.controller.COLORS['background'])
        self.content_frame.pack(side='right', fill='both', expand=True)
        
    def show(self):
        self.root.deiconify()  # Show the main window
        
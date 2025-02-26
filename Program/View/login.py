import tkinter as tk
from tkinter import messagebox

class LoginView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Toplevel()
        self.root.title("EUNOIA - We Care")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.minsize(900, 600)
        
        self.root.withdraw()
        
        self.root.configure(bg=self.controller.COLORS['background'])
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main container with modern shadow effect
        container = tk.Frame(
            self.root,
            bg=self.controller.COLORS['background'],
            highlightbackground=self.controller.COLORS['light_gray'],
            highlightthickness=1
        )
        container.place(relx=0.5, rely=0.5, anchor='center')
        
        # Left panel with gradient-like effect
        left_panel = tk.Frame(container, bg=self.controller.COLORS['primary'], width=400, height=500)
        left_panel.pack(side='left', fill='y')
        left_panel.pack_propagate(False)
        
        # Decorative circles for modern look
        canvas = tk.Canvas(
            left_panel, 
            width=400, 
            height=500, 
            bg=self.controller.COLORS['primary'], 
            highlightthickness=0
        )
        canvas.place(x=0, y=0)
        
        # App name with modern styling
        app_name = tk.Label(
            left_panel,
            text="EUNOIA",
            font=self.controller.FONTS['title'],
            bg=self.controller.COLORS['primary'],
            fg='white'
        )
        app_name.pack(pady=(100, 5))
        
        # Welcome text
        welcome_text = tk.Label(
            left_panel,
            text="Welcome Back",
            font=self.controller.FONTS['heading'],
            bg=self.controller.COLORS['primary'],
            fg='white'
        )
        welcome_text.pack(pady=(20, 5))
        
        # Subtitle
        subtitle = tk.Label(
            left_panel,
            text="Sign in to continue access",
            font=self.controller.FONTS['subheading'],
            bg=self.controller.COLORS['primary'],
            fg='white'
        )
        subtitle.pack()
        
        right_panel = tk.Frame(container, bg='white', width=400, height=500)
        right_panel.pack(side='right', fill='y')
        right_panel.pack_propagate(False)
        
        # Sign In text
        sign_in = tk.Label(
            right_panel,
            text="Sign In",
            font=self.controller.FONTS['heading'],
            bg='white',
            fg=self.controller.COLORS['text']
        )
        sign_in.pack(pady=(100, 40))
        
        # Username entry
        self.username_entry = self.create_modern_entry(right_panel, "Email Address")
        
        # Password entry
        self.password_entry = self.create_modern_entry(right_panel, "Password", show="●")
        
        # Login button
        login_btn = tk.Button(
            right_panel,
            text="CONTINUE",
            font=self.controller.FONTS['button'],
            bg=self.controller.COLORS['primary'],
            fg='white',
            relief='flat',
            command=self.login,
            cursor='hand2',
            padx=30,
            pady=12
        )
        login_btn.pack(pady=30)
        
        # Register link
        register_link = tk.Label(
            right_panel,
            text="Don't have an account? Register here",
            font=self.controller.FONTS['small'],
            bg='white',
            fg=self.controller.COLORS['text'],
            cursor='hand2'
        )
        register_link.pack(pady=10)
        register_link.bind('<Button-1>', lambda e: self.controller.show_sign_up())
        
    def create_modern_entry(self, parent, placeholder, show=None):
        frame = tk.Frame(parent, bg='white')
        frame.pack(fill='x', padx=40, pady=10)
        
        entry = tk.Entry(
            frame,
            font=self.controller.FONTS['body'],
            bg='white',
            fg=self.controller.COLORS['text'],
            insertbackground=self.controller.COLORS['text'],
            relief='flat',
            show=show
        )
        
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(entry, placeholder))
        entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(entry, placeholder))
        entry.pack(fill='x', pady=(5, 0))
        
        underline = tk.Frame(frame, height=2, bg=self.controller.COLORS['light_gray'])
        underline.pack(fill='x', pady=(2, 0))
        
        entry.bind('<Enter>', lambda e: underline.configure(bg=self.controller.COLORS['primary']))
        entry.bind('<Leave>', lambda e: underline.configure(bg=self.controller.COLORS['light_gray']))
        
        return entry
        
    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            if placeholder == "Password":
                entry.config(show="●")
            entry.config(fg=self.controller.COLORS['text'])
            
    def on_entry_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Password":
                entry.config(show="")
            entry.config(fg='gray')
            
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in ["Email Address", ""] or password in ["Password", ""]:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        try:
            if self.controller.login(username, password):
                self.clear_entries()
                self.hide()
                self.controller.show_main_window()
            else:
                messagebox.showerror("Error", "Invalid email or password")
        except Exception as e:
            messagebox.showerror("Error", f"Login failed: {str(e)}")
            
    def clear_entries(self):
        self.username_entry.delete(0, 'end')
        self.username_entry.insert(0, "Email Address")
        self.password_entry.delete(0, 'end')
        self.password_entry.insert(0, "Password")
        self.password_entry.config(show="")
        
    def show(self):
        self.clear_entries()  
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
    def hide(self):
        self.root.withdraw()
        
    def on_close(self):
        self.hide()
        self.controller.quit()

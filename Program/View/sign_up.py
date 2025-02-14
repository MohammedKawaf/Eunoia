import tkinter as tk
from tkinter import messagebox

class SignUpView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Toplevel()
        self.root.title("EUNOIA - Register")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        self.root.minsize(900, 600)
        
        # Configure root background
        self.root.configure(bg=self.controller.COLORS['background'])
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create register container
        register_frame = tk.Frame(self.root, bg=self.controller.COLORS['background'])
        register_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # App name
        app_name = tk.Label(
            register_frame,
            text="EUNOIA",
            font=('Times New Roman', 48, 'bold'),
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['primary']
        )
        app_name.pack(pady=(0, 5))
        
        # Tagline
        tagline = tk.Label(
            register_frame,
            text="WE CARE",
            font=('Arial', 14, 'normal'),
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['text']
        )
        tagline.pack(pady=(0, 30))
        
        # Title
        title = tk.Label(
            register_frame,
            text="Create Account",
            font=('Helvetica', 24, 'bold'),
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['text']
        )
        title.pack(pady=20)
        
        # Username entry
        username_frame, self.username_entry = self.create_modern_entry(register_frame, "Username")
        username_frame.pack(pady=10)
        
        # Password entry
        password_frame, self.password_entry = self.create_modern_entry(register_frame, "Password")
        self.password_entry.configure(show="●")
        password_frame.pack(pady=10)
        
        # Register button
        register_btn = self.create_modern_button(register_frame, "Register", self.register)
        register_btn.pack(pady=20)
        
        # Login link
        login_link = tk.Label(
            register_frame,
            text="Already have an account? Login here",
            font=('Helvetica', 10, 'underline'),
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['text'],
            cursor='hand2'
        )
        login_link.pack(pady=10)
        login_link.bind('<Button-1>', lambda e: self.show_login())

    # Creates a modern styled entry field with placeholder text
    def create_modern_entry(self, parent, placeholder):
        frame = tk.Frame(
            parent,
            bg=self.controller.COLORS['card_shadow'],
            highlightthickness=1,
            highlightbackground=self.controller.COLORS['light_gray']
        )
        
        entry = tk.Entry(
            frame,
            font=self.controller.FONTS['body'],
            bg=self.controller.COLORS['background'],
            fg="gray",
            relief='flat',
            width=30,
            insertbackground=self.controller.COLORS['primary']
        )
        
        entry.insert(0, placeholder)
        entry.bind('<FocusIn>', lambda e: self.on_entry_focus_in(entry, placeholder))
        entry.bind('<FocusOut>', lambda e: self.on_entry_focus_out(entry, placeholder))
        entry.pack(padx=2, pady=2, ipady=8)
        
        return frame, entry

    # Creates a modern styled button with hover effects   
    def create_modern_button(self, parent, text, command):
        btn_frame = tk.Frame(parent, bg=self.controller.COLORS['card_shadow'])
        
        button = tk.Button(
            btn_frame,
            text=text,
            command=command,
            bg=self.controller.COLORS['primary'],
            fg='white',
            font=self.controller.FONTS['button'],
            relief='flat',
            cursor='hand2',
            padx=20,
            pady=10,
            borderwidth=0
        )
        button.pack(padx=1, pady=1)
        
        # Hover effects
        def on_enter(e):
            button.configure(
                bg=self.controller.adjust_color(self.controller.COLORS['primary'], -20)
            )
            btn_frame.configure(
                bg=self.controller.adjust_color(self.controller.COLORS['card_shadow'], -10)
            )
            
        def on_leave(e):
            button.configure(bg=self.controller.COLORS['primary'])
            btn_frame.configure(bg=self.controller.COLORS['card_shadow'])
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return btn_frame

    # Clears the placeholder text when the entry field gains focus
    def on_entry_focus_in(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            if placeholder == "Password":
                entry.config(show="●")
            entry.configure(fg=self.controller.COLORS['text'])

    # Restores the placeholder text if the entry field loses focus and is empty      
    def on_entry_focus_out(self, entry, placeholder):
        if entry.get() == "":
            entry.insert(0, placeholder)
            if placeholder == "Password":
                entry.config(show="")
            entry.configure(fg='gray')

    # Handles user registration by checking input and adding the user to the database
    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username in ["Username", ""] or password in ["Password", ""]:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if self.controller.register(username, password):
            messagebox.showinfo("Success", "Registration successful!")
            self.show_login()
        else:
            messagebox.showerror("Error", "Username already exists")

    # Makes the window visible     
    def show(self):
        self.root.deiconify()

    # Hides the window   
    def hide(self):
        self.root.withdraw()

    # Shows the login view
    def show_login(self):
        """Visar login-vyn"""
        self.controller.show_login()
import tkinter as tk
from tkinter import ttk, messagebox

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
        self.create_menu()
        
        # Create content frame
        self.content_frame = tk.Frame(self.main_frame, bg=self.controller.COLORS['background'])
        self.content_frame.pack(side='right', fill='both', expand=True)
        
        # Show mood assessment first
        self.show_mood_assessment()
        
    def create_menu(self):
        # Create menu frame
        menu_frame = tk.Frame(self.main_frame, bg=self.controller.COLORS['primary'], width=250)
        menu_frame.pack(side='left', fill='y', padx=20, pady=20)
        menu_frame.pack_propagate(False)
        
        # App name in menu
        app_name = tk.Label(
            menu_frame,
            text="EUNOIA",
            font=('Times New Roman', 28, 'bold'),
            bg=self.controller.COLORS['primary'],
            fg='white'
        )
        app_name.pack(pady=(30, 5))
        
        # Tagline
        tagline = tk.Label(
            menu_frame,
            text="WE CARE",
            font=('Arial', 10, 'normal'),
            bg=self.controller.COLORS['primary'],
            fg='white'
        )
        tagline.pack(pady=(0, 30))
        
        # Menu buttons
        self.create_menu_button(menu_frame, "📋 Tasks", self.show_todo_content)
        
        # Logout button
        logout_btn = tk.Button(
            menu_frame,
            text="🚪 Logout",
            command=self.controller.logout,
            bg='white',
            fg=self.controller.COLORS['primary'],
            font=('Arial', 12, 'bold'),
            relief='flat',
            borderwidth=0,
            padx=20,
            pady=10,
            cursor='hand2'
        )
        logout_btn.pack(side='bottom', pady=20)
        
    def create_menu_button(self, parent, text, command):
        btn_frame = tk.Frame(parent, bg=self.controller.COLORS['primary'])
        btn_frame.pack(fill='x', pady=5, padx=10)
        
        btn = tk.Button(
            btn_frame,
            text=text,
            command=command,
            bg=self.controller.COLORS['primary'],
            fg='white',
            font=('Helvetica', 14, 'bold'),
            relief='flat',
            cursor='hand2',
            anchor='w',
            padx=20,
            pady=15
        )
        btn.pack(fill='x')
        
        # Hover effects
        btn.bind('<Enter>', lambda e: btn.configure(
            bg=self.controller.adjust_color(self.controller.COLORS['primary'], -20)
        ))
        btn.bind('<Leave>', lambda e: btn.configure(
            bg=self.controller.COLORS['primary']
        ))
        
        return btn
        
    def show_mood_assessment(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Create mood frame
        mood_frame = tk.Frame(self.content_frame, bg=self.controller.COLORS['background'])
        mood_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title = tk.Label(
            mood_frame,
            text="How are you feeling today?",
            font=self.controller.FONTS['heading'],
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['text']
        )
        title.pack(pady=(0, 30))
        
        # Mood scale
        self.mood_var = tk.StringVar(value="3")
        mood_scale = tk.Scale(
            mood_frame,
            from_=1,
            to=5,
            orient='horizontal',
            length=300,
            variable=self.mood_var,
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['text'],
            highlightthickness=0,
            command=self.update_mood_description
        )
        mood_scale.pack()
        
        # Mood description
        self.mood_description = tk.Label(
            mood_frame,
            text="Neutral",
            font=self.controller.FONTS['subheading'],
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['text']
        )
        self.mood_description.pack(pady=20)
        
        # Continue button
        continue_btn = self.create_modern_button(
            mood_frame,
            "Continue to Tasks",
            lambda: self.show_todo_content(self.mood_var.get())
        )
        continue_btn.pack(pady=30)
        
    def update_mood_description(self, value):
        mood_descriptions = {
            '1': "Very Low - Need extra care today",
            '2': "Low - Could use some uplift",
            '3': "Neutral - Balanced",
            '4': "Good - Positive energy",
            '5': "Excellent - Feeling great!"
        }
        self.mood_description.config(
            text=mood_descriptions.get(str(int(float(value))), "Neutral")
        )
        
    def create_modern_button(self, parent, text, command, color=None):
        if color is None:
            color = self.controller.COLORS['primary']
            
        btn_frame = tk.Frame(parent, bg=self.controller.COLORS['card_shadow'])
        
        button = tk.Button(
            btn_frame,
            text=text,
            command=command,
            bg=color,
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
            button.configure(bg=self.controller.adjust_color(color, -20))
            btn_frame.configure(bg=self.controller.adjust_color(
                self.controller.COLORS['card_shadow'], -10
            ))
            
        def on_leave(e):
            button.configure(bg=color)
            btn_frame.configure(bg=self.controller.COLORS['card_shadow'])
            
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        
        return btn_frame
    
    def show_todo_content(self, mood_value=None):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Spara mood-värdet om det finns
        if mood_value:
            self.controller.set_current_mood(mood_value)
            
        # Create scrollable frame
        canvas = tk.Canvas(self.content_frame, bg=self.controller.COLORS['background'])
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.controller.COLORS['background'])
        
        # Konfigurera canvas för att expandera
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind mouse wheel event för scrollning
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # Konfigurera canvas för att anpassa innehållet
        def configure_canvas(event):
            canvas.configure(width=event.width)
            canvas.itemconfig(frame_id, width=event.width)
        
        canvas.bind('<Configure>', configure_canvas)
        
        # Skapa fönster i canvas
        frame_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        
        # Create todo container
        todo_frame = tk.Frame(scrollable_frame, bg=self.controller.COLORS['background'])
        todo_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header med välkomstmeddelande och humörbeskrivning
        if mood_value:
            mood_description = self.controller.get_mood_description(mood_value)
            mood_label = tk.Label(
                todo_frame,
                text=f"Today's mood: {mood_description}",
                font=self.controller.FONTS['subheading'],
                bg=self.controller.COLORS['background'],
                fg=self.controller.COLORS['text']
            )
            mood_label.pack(pady=(0, 20))
        
        # Visa rekommendationer baserat på humör
        recommendations = self.controller.get_mood_recommendations()
        if recommendations:
            rec_frame = tk.Frame(todo_frame, bg=self.controller.COLORS['light_gray'])
            rec_frame.pack(fill='x', pady=(0, 20), padx=10)
            
            rec_title = tk.Label(
                rec_frame,
                text="Recommended activities for today's mood: ",
                font=self.controller.FONTS['subheading'],
                bg=self.controller.COLORS['light_gray'],
                fg=self.controller.COLORS['text']
            )
            rec_title.pack(pady=(10, 5), padx=10, anchor='w')
            
            for rec in recommendations:
                rec_label = tk.Label(
                    rec_frame,
                    text=f"• {rec}",
                    font=self.controller.FONTS['body'],
                    bg=self.controller.COLORS['light_gray'],
                    fg=self.controller.COLORS['text'],
                    wraplength=600,
                    justify='left'
                )
                rec_label.pack(anchor='w', padx=20, pady=2)
        
        # Lägg till ny task-sektion
        add_frame = tk.Frame(todo_frame, bg=self.controller.COLORS['background'])
        add_frame.pack(fill='x', pady=20)
        
        self.task_entry = tk.Entry(
            add_frame,
            font=self.controller.FONTS['body'],
            bg=self.controller.COLORS['light_gray'],
            fg=self.controller.COLORS['text'],
            relief='flat'
        )
        self.task_entry.pack(side='left', expand=True, fill='x', padx=(0, 10))
        
        add_btn = self.create_modern_button(
            add_frame,
            "Add Task",
            self.add_todo,
            self.controller.COLORS['success']
        )
        add_btn.pack(side='right')
        
        # Visa befintliga tasks
        tasks_label = tk.Label(
            todo_frame,
            text="My tasks: ",
            font=self.controller.FONTS['subheading'],
            bg=self.controller.COLORS['background'],
            fg=self.controller.COLORS['text']
        )
        tasks_label.pack(pady=(20, 10), anchor='w')
        
        self.todos_frame = tk.Frame(todo_frame, bg=self.controller.COLORS['light_gray'])
        self.todos_frame.pack(fill='both', expand=True, pady=10)
        
        self.update_todos_list()
        
    def add_todo(self):
        task = self.task_entry.get().strip()
        if task:
            if self.controller.save_todo(task):
                self.task_entry.delete(0, 'end')
                self.update_todos_list()
                
    def update_todos_list(self):
        # Clear existing todos
        for widget in self.todos_frame.winfo_children():
            widget.destroy()
            
        # Get and display todos
        todos = self.controller.get_todos()
        if todos:
            for todo in todos:
                todo_item = tk.Frame(
                    self.todos_frame,
                    bg=self.controller.COLORS['background']
                )
                todo_item.pack(fill='x', pady=2)
                
                done_var = tk.BooleanVar(value=todo['done'])
                checkbox = tk.Checkbutton(
                    todo_item,
                    var=done_var,
                    command=lambda t=todo: self.controller.toggle_todo(t),
                    bg=self.controller.COLORS['background']
                )
                checkbox.pack(side='left')
                
                task_label = tk.Label(
                    todo_item,
                    text=todo['task'],
                    font=self.controller.FONTS['body'],
                    bg=self.controller.COLORS['background'],
                    fg=self.controller.COLORS['text']
                )
                task_label.pack(side='left', padx=5)
                
                delete_btn = tk.Button(
                    todo_item,
                    text="×",
                    command=lambda t=todo: self.delete_todo(t),
                    bg=self.controller.COLORS['background'],
                    fg=self.controller.COLORS['warning'],
                    relief='flat',
                    cursor='hand2'
                )
                delete_btn.pack(side='right')
        
    def delete_todo(self, todo):
        if messagebox.askyesno("Confirm", "Delete this task?"):
            self.controller.delete_todo(todo)
            self.update_todos_list()
            
    def show(self):
        self.root.deiconify()  # Show the main window
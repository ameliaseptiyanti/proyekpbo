import tkinter as tk
from tkinter import messagebox

class Login:
    def __init__(self, chat_app, padding=20):
        self.chat_app = chat_app
        self.frame = tk.Frame(chat_app.root)
        self.frame_width = 300  # Tentukan lebar formulir
        self.frame_height = 200  # Tentukan tinggi formulir
        self.chat_app = chat_app

        self.login_frame = tk.Frame(self.chat_app.root)
        self.login_frame.place(relx=0.5, rely=0.3, anchor="center")  # Set position of login frame on top
        

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "" and password == "":
            self.chat_app.show_navigation_bar(username)
            self.destroy()  # Add this line to destroy the login frame after successful login
            messagebox.showinfo("Info", "Login successful!")
        else:
            messagebox.showerror("Error", "Login failed. Username or password is incorrect.")
    def get_frame_width(self):
        return self.frame_width

    def get_frame_height(self):
        return self.frame_height
    
    def destroy(self):
        self.login_frame.destroy()

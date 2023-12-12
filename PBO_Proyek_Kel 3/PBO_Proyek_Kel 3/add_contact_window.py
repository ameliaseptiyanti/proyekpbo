import tkinter as tk
from tkinter import ttk, messagebox
from chat_window import ChatWindow

class AddContactWindow:
    def __init__(self, root, chat_app):
        self.root = root
        self.chat_app = chat_app

        self.add_contact_window = tk.Toplevel(root)
        self.add_contact_window.title("Add Contact")
        self.add_contact_window.configure(bg="#f0f0f0")  # Set background color

        # Main Frame
        main_frame = tk.Frame(self.add_contact_window, bg="#f0f0f0")
        main_frame.pack(padx=10, pady=10)

        # Username Entry
        self.username_label = tk.Label(main_frame, text="Username:", bg="#f0f0f0", font=("Arial", 12))
        self.username_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

        self.username_entry = tk.Entry(main_frame, font=("Arial", 12))
        self.username_entry.grid(row=0, column=1, pady=(0, 5))

        # Add Button
        self.add_button = tk.Button(main_frame, text="Add", command=self.add_contact, bg="#4CAF50", fg="white", font=("Arial", 12))  # Green button
        self.add_button.grid(row=1, column=0, columnspan=2, pady=(5, 10), sticky="nsew")

        # Open Chat Button
        self.open_chat_button = tk.Button(main_frame, text="Open Chat", command=self.open_chat, bg="#007BFF", fg="white", font=("Arial", 12))  # Blue button
        self.open_chat_button.grid(row=2, column=0, columnspan=2, pady=(0, 10), sticky="nsew")

        # Contact List Treeview
        self.contact_tree = ttk.Treeview(main_frame, columns=("Username", "Avatar"), show="headings", selectmode="browse")
        self.contact_tree.heading("Username", text="Username", anchor="w")  # Set anchor to west (left)
        self.contact_tree.column("Username", width=120, anchor="w")
        self.contact_tree.heading("Avatar", text="Avatar")
        self.contact_tree.column("Avatar", width=50, anchor="center")
        self.contact_tree.grid(row=3, column=0, columnspan=2, pady=(0, 10), sticky="nsew")

        self.update_contact_list()

    def add_contact(self):
        new_contact = self.username_entry.get()
        if new_contact not in self.chat_app.users and new_contact not in self.chat_app.group_members:
            self.chat_app.users[new_contact] = {"password": "password", "chat_window": None}
            messagebox.showinfo("Info", "Contact added successfully!")
            self.update_contact_list()
        else:
            messagebox.showerror("Error", "Invalid username or contact already exists.")

    def open_chat(self):
        selected_contact = self.contact_tree.selection()
        if selected_contact:
            selected_contact = self.contact_tree.item(selected_contact, "values")[0]
            if selected_contact in self.chat_app.group_members:
                self.chat_app.show_group_chat_page(selected_contact)
            elif self.chat_app.users[selected_contact]["chat_window"] is None:
                chat_window = tk.Toplevel(self.root)
                chat_window.title(f"Chat Window - {selected_contact}")
                self.chat_app.users[selected_contact]["chat_window"] = ChatWindow(chat_window, self.chat_app, selected_contact)
        else:
            messagebox.showerror("Error", "Please select a contact to open chat.")

    def update_contact_list(self):
        # Clear existing items
        for item in self.contact_tree.get_children():
            self.contact_tree.delete(item)

        # Populate with new data
        for contact in self.chat_app.users:
            if contact not in self.chat_app.group_members and contact not in ["User1", "User2"]:
                avatar_image = tk.PhotoImage(width=30, height=30)  # Placeholder avatar
                self.contact_tree.insert("", "end", values=(contact, avatar_image))
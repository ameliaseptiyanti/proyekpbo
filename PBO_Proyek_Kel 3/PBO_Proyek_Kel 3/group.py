import tkinter as tk
from tkinter import messagebox

class GroupManager(tk.Toplevel):
    def __init__(self, root, chat_app):
        super().__init__(root)
        self.title("Group Options")
        self.chat_app = chat_app
        self.group_name = None  # Simpan nama grup yang diklik di sini
        self.group_name_label = tk.Label(self, text="Selected Group:")
        self.group_name_label.pack()
        self.group_name_entry = tk.Entry(self, state="disabled")
        self.group_name_entry.pack()
        self.enter_chat_button = tk.Button(self, text="Enter Group Chat", command=self.enter_group_chat)
        self.enter_chat_button.pack()
        self.add_member_button = tk.Button(self, text="Add Group Member", command=self.add_group_member)
        self.add_member_button.pack()
        self.create_group_button = tk.Button(self, text="Create Group", command=self.create_group)
        self.create_group_button.pack()
        self.delete_member_button = tk.Button(self, text="Delete Group Member", command=self.delete_group_member)
        self.delete_member_button.pack()



    def create_group(self):
        group_name = self.group_name_entry.get()
        if group_name:
            # Lakukan logika pembuatan grup
            self.chat_app.create_group(group_name)
            messagebox.showinfo("Info", f"Group '{group_name}' has been created!")
            self.destroy()
        else:
            messagebox.showerror("Error", "Please provide a group name!")

    def set_selected_group(self, group_name):
        self.group_name = group_name
        self.group_name_entry.configure(state="normal")
        self.group_name_entry.delete(0, tk.END)
        self.group_name_entry.insert(0, group_name)
        self.group_name_entry.configure(state="disabled")

    def enter_group_chat(self):
        if self.group_name:
            messagebox.showinfo("Info", f"Entering Group Chat '{self.group_name}'!")
            # Logika untuk masuk ke obrolan grup
            self.destroy()
        else:
            messagebox.showerror("Error", "Please select a group to enter!")

    def add_group_member(self):
        if self.group_name:
            self.chat_app.show_add_members_page(self.group_name)
            self.destroy()
        else:
            messagebox.showerror("Error", "Please select a group to add members!")

    

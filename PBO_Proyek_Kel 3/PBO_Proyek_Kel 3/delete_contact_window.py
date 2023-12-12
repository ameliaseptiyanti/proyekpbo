import tkinter as tk
from tkinter import messagebox
from chat_window import ChatWindow  # Import ChatWindow here

class DeleteContactWindow:
    def __init__(self, root, chat_app, add_contact_window):
        self.root = root
        self.chat_app = chat_app
        self.add_contact_window = add_contact_window

        self.delete_contact_window = tk.Toplevel(root)
        self.delete_contact_window.title("Delete Contact")
        self.delete_contact_window.configure(bg="#f0f0f0")  # Set background color

        # Main Frame
        main_frame = tk.Frame(self.delete_contact_window, bg="#f0f0f0")
        main_frame.pack(padx=10, pady=10)

        # Select Contact Label
        self.username_label = tk.Label(main_frame, text="Select Contact:", bg="#f0f0f0", font=("Arial", 12))
        self.username_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Contact Listbox
        self.contact_listbox = tk.Listbox(main_frame, bg="white", font=("Arial", 12), selectbackground="#a6a6a6")
        self.contact_listbox.grid(row=1, columnspan=2, pady=10, sticky="nsew")
        self.update_contact_list()

        # Delete Button
        self.delete_button = tk.Button(main_frame, text="Delete", command=self.confirm_delete_contact, bg="#FF3333", fg="white", font=("Arial", 12))  # Red button
        self.delete_button.grid(row=2, columnspan=2, pady=(5, 10), sticky="nsew")

    def update_contact_list(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.chat_app.users:
            if contact not in self.chat_app.group_members and contact not in ["User1", "User2"]:
                self.contact_listbox.insert(tk.END, contact)

    def confirm_delete_contact(self):
        selected_contact = self.contact_listbox.get(tk.ACTIVE)
        if selected_contact:
            confirm_delete = messagebox.askyesno("Confirmation", f"Are you sure you want to delete {selected_contact}?")
            if confirm_delete:
                self.delete_contact(selected_contact)
        else:
            messagebox.showerror("Error", "Please select a contact to delete.")

    def delete_contact(self, selected_contact):
        del self.chat_app.users[selected_contact]
        messagebox.showinfo("Info", f"Contact {selected_contact} deleted successfully!")
        self.update_contact_list()
        self.add_contact_window.update_contact_list()

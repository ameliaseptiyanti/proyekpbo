# chat_app.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from chat_window import ChatWindow
from group_chat_manager import GroupChatManager
from add_contact_window import AddContactWindow
from delete_contact_window import DeleteContactWindow
from settings import Setting
from login import Login

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat App")
        self.users = {}
        self.group_chat_windows = {}
        self.group_members = {}
        self.add_contact_window = None
        self.delete_contact_window = None
        self.nav_bar = None
        self.login_frame = None
        self.chat_buttons = []
        self.chat_messages = {}
        self.group_listbox = None
        self.group_manager = GroupChatManager(self.root, self)
        # Set the window size to a common smartphone resolution (Full HD)
        smartphone_resolution = (480, 854)
        self.root.geometry(f"{smartphone_resolution[0]}x{smartphone_resolution[1]}")

        # Load the background image
        bg_image = Image.open("BG1.png")
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a Label to display the background image
        self.bg_label = tk.Label(root, image=bg_photo)
        self.bg_label.image = bg_photo
        self.bg_label.place(relwidth=1, relheight=1)  # Set label size to cover the entire window

        self.login_setup()

        self.setup_appearance_defaults()

    def setup_appearance_defaults(self):
        self.theme_var = tk.StringVar(value="Light")
        self.text_color_var = tk.StringVar(value="Black")
        self.font_size_var = tk.StringVar(value="Medium")

    def login(self):
        username = self.login_frame.username_entry.get()
        password = self.login_frame.password_entry.get()

        if username not in self.users:
            self.users[username] = {"password": password, "chat_window": None}
            self.setup_appearance_defaults()  # Move this line to set appearance defaults on login
            messagebox.showinfo("Info", "Login successful!")
            self.show_navigation_bar(username)
        else:
            messagebox.showerror("Error", "Login failed. Username already in use.")


    def login_setup(self):
        self.login_frame = Login(self, padding=20)

        # Find the screen size
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate the position x dan y untuk menempatkan frame login di tengah layar
        x_position = (screen_width - self.login_frame.get_frame_width()) // 2
        y_position = (screen_height - self.login_frame.get_frame_height()) // 2

        # Place the login frame in the center of the screen
        self.login_frame.frame.place(x=x_position, y=y_position)

    def show_navigation_bar(self, username):
        self.login_frame.destroy()

        # Set the background color
        bg_color = "black" if self.theme_var.get().lower() == "dark" else "white"
        self.root.configure(bg=bg_color)

        self.nav_bar = ttk.Notebook(self.root)
        self.nav_bar.pack(fill=tk.X, padx=10, pady=10)  # Set fill to tk.X to expand horizontally

        self.create_navigation_tabs(username)

    def create_navigation_tabs(self, username):
        self.create_chat_tab(username)
        self.create_group_tab()
        self.create_contact_tabs()
        self.create_settings_tab()  # Add this line to create the settings tab

        # Set the background image for all tabs
        for i in range(len(self.nav_bar.winfo_children())):
            tab_frame = self.nav_bar.winfo_children()[i]
            bg_image = Image.open("BG1.png")
            bg_photo = ImageTk.PhotoImage(bg_image)

            bg_label = tk.Label(tab_frame, image=bg_photo)
            bg_label.image = bg_photo
            bg_label.place(relwidth=1, relheight=1)

            # Move the background label to the back
            bg_label.lower()


    def create_chat_tab(self, username):
        chat_frame = tk.Frame(self.nav_bar)
        self.nav_bar.add(chat_frame, text="Chat")
        # Load the background image
        bg_image = Image.open("BG1.png")
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Create a Label to display the background image
        bg_label = tk.Label(chat_frame, image=bg_photo)
        bg_label.image = bg_photo
        bg_label.place(relwidth=1, relheight=1)

        # Display individual and group chats
        chats_label = tk.Label(chat_frame, text="Chats", font=("Helvetica", 14, "bold"), bg="lightgray")
        chats_label.pack(pady=10)

        # Create a Listbox to display individual and group chats
        chat_listbox = tk.Listbox(chat_frame, selectmode="single", height=20, width=50, bg="white")
        chat_listbox.pack(padx=10, pady=10)

        # Add individual chats to the Listbox
        for user in self.users.keys():
            if user != username:
                chat_listbox.insert(tk.END, f"Chat with {user}")

        # Add group chats to the Listbox
        for group_name in self.group_chat_windows.keys():
            chat_listbox.insert(tk.END, f"Group chat: {group_name}")

        # Add contacts to the Listbox
        contacts_label = tk.Label(chat_frame, text="Contacts", font=("Helvetica", 14, "bold"), bg="lightgray")
        contacts_label.pack(pady=10)

        for contact in self.get_contact_list():
            chat_listbox.insert(tk.END, f"Chat with {contact}")

        # Bind a function to handle chat selection
        chat_listbox.bind("<Double-Button-1>", self.open_selected_chat)

    def open_selected_chat(self, event):
        selected_index = event.widget.curselection()
        if selected_index:
            selected_chat = event.widget.get(selected_index)
            if selected_chat.startswith("Chat with"):
                other_user = selected_chat.split(" ")[-1]
                self.open_chat_window(other_user)
            elif selected_chat.startswith("Group chat:"):
                group_name = selected_chat.split(" ")[-1]
                self.show_group_chat_page(group_name)
            elif selected_chat.startswith("Chat with"):
                contact = selected_chat.split(" ")[-1]
                self.open_chat_window(contact)
                
    def open_chat_window(self, other_user):
        data = self.users.get(other_user, {})
        if data and data["chat_window"] is None:
            chat_window = tk.Toplevel(self.root)
            chat_window.title(f"Chat Window - {other_user}")
            data["chat_window"] = ChatWindow(chat_window, self, other_user)
        elif data and data["chat_window"] and data["chat_window"].root.winfo_exists():
            data["chat_window"].root.deiconify()

    def reset_chat(self, username):
        # Called when the window is closed to reset the chat window
        if username in self.users and self.users[username]["chat_window"]:
            # Destroy the existing chat window
            self.users[username]["chat_window"].root.destroy()

            # Set the chat_window attribute to None
            self.users[username]["chat_window"] = None

    def create_group_tab(self):
        group_frame = tk.Frame(self.nav_bar, bg="lightgray")
        self.nav_bar.add(group_frame, text="Groups")
        

        # UI elements for managing groups
        
        create_group_button = tk.Button(group_frame, text="Create Group", command=self.create_group, bg="green", fg="white")
        create_group_button.pack(pady=10)

        group_listbox = tk.Listbox(group_frame, selectmode="single", height=10, width=30, bg="white")
        group_listbox.pack(padx=10, pady=10)

        # Update the listbox with existing groups
        for group_name in self.group_chat_windows.keys():
            group_listbox.insert(tk.END, group_name)

    def create_contact_tabs(self):
        contacts_frame = tk.Frame(self.nav_bar, bg="lightgray")
        self.nav_bar.add(contacts_frame, text="Contacts")

        # UI elements for managing contacts
        add_contact_button = tk.Button(contacts_frame, text="Add Contact", command=self.show_add_contact_page, bg="blue", fg="white")
        add_contact_button.pack(pady=10)

        delete_contact_button = tk.Button(contacts_frame, text="Delete Contact", command=self.show_delete_contact_page, bg="red", fg="white")
        delete_contact_button.pack(pady=10)

        # Add more UI elements as needed

    def create_settings_tab(self):
        settings_frame = tk.Frame(self.nav_bar, bg="lightgray")
        self.nav_bar.add(settings_frame, text="Settings")

        # UI elements for settings
        theme_label = tk.Label(settings_frame, text="Theme:")
        theme_label.pack(pady=10)

        theme_combobox = ttk.Combobox(settings_frame, textvariable=self.theme_var, values=["Light", "Dark"])
        theme_combobox.pack(pady=10)

        text_color_label = tk.Label(settings_frame, text="Text Color:")
        text_color_label.pack(pady=10)

        text_color_combobox = ttk.Combobox(settings_frame, textvariable=self.text_color_var, values=["Black", "White"])
        text_color_combobox.pack(pady=10)

        font_size_label = tk.Label(settings_frame, text="Font Size:")
        font_size_label.pack(pady=10)

        font_size_combobox = ttk.Combobox(settings_frame, textvariable=self.font_size_var, values=["Small", "Medium", "Large"])
        font_size_combobox.pack(pady=10)

        apply_button = tk.Button(settings_frame, text="Apply Settings", command=self.apply_appearance_settings)
        apply_button.pack(pady=10)

    def create_group(self):
        create_group_window = tk.Toplevel(self.root)
        create_group_window.title("Create Group")

        group_name_label = tk.Label(create_group_window, text="Group Name:")
        group_name_label.grid(row=0, column=0, sticky="w")

        group_name_entry = tk.Entry(create_group_window)
        group_name_entry.grid(row=0, column=1, pady=10)

        add_members_button = tk.Button(create_group_window, text="Add Members", command=lambda: self.show_add_members_page(group_name_entry.get()))
        add_members_button.grid(row=1, columnspan=2)

        create_button = tk.Button(create_group_window, text="Create", command=lambda: self.handle_create_group(group_name_entry.get(), create_group_window))
        create_button.grid(row=2, columnspan=2)

    def handle_create_group(self, group_name, window):
       
        if group_name and group_name not in self.group_chat_windows:
            selected_members = self.show_add_members_page(group_name)
            if selected_members:
                self.group_members[group_name] = selected_members
                self.show_group_chat_page(group_name)
                self.update_group_listbox()  # Tambahkan ini untuk memperbarui Listbox
                window.destroy()
            else:
                messagebox.showerror("Error", "Please select members to add to the group.")
        else:
            messagebox.showerror("Error", "Invalid group name or group already exists.")

       
    
    def update_group_listbox(self):
        # Ambil Listbox di bawah tombol "Create Group" di tab "Groups"
        if self.nav_bar and self.nav_bar.winfo_children():
            group_frame = self.nav_bar.winfo_children()[1]  # Indeks ini mungkin perlu disesuaikan dengan posisi Listbox di GUI Anda

            # Bersihkan isi Listbox
            for widget in group_frame.winfo_children():
                if isinstance(widget, tk.Listbox):
                    widget.delete(0, tk.END)

            # Perbarui dengan nama grup yang ada sekarang
            for group_name in self.group_chat_windows.keys():
                for widget in group_frame.winfo_children():
                    if isinstance(widget, tk.Listbox):
                        widget.insert(tk.END, group_name)

    def update_group_tab(self):
        # Fungsi ini akan memperbarui Listbox di tab "Groups" dengan daftar grup yang diperbarui
        if self.nav_bar and self.group_listbox:  
            group_listbox = self.group_listbox

            # Hapus item-item yang ada
            group_listbox.delete(0, tk.END)

            # Perbarui dengan nama grup yang ada sekarang
            for group_name in self.group_chat_windows.keys():
                group_listbox.insert(tk.END, group_name)


    def show_add_members_page(self, group_name):
        add_members_window = tk.Toplevel(self.root)
        add_members_window.title(f"Add Members to {group_name}")

        username_label = tk.Label(add_members_window, text="Username:")
        username_label.grid(row=0, column=0, sticky="w")

        username_entry = tk.Entry(add_members_window)
        username_entry.grid(row=0, column=1, pady=10)

        def add_member_to_group_wrapper():
            self.add_member_to_group(group_name, username_entry.get(), add_members_window)

        add_button = tk.Button(add_members_window, text="Add", command=add_member_to_group_wrapper)
        add_button.grid(row=1, columnspan=2)

        member_listbox = tk.Listbox(add_members_window, selectmode="multiple")
        member_listbox.grid(row=2, columnspan=2, pady=10)

        for contact in self.get_contact_list():
            member_listbox.insert(tk.END, contact)

        return member_listbox

    def add_member_to_group(self, group_name, username, window):
        if username and str(username) not in self.group_members.get(group_name, []): 
            self.group_members.setdefault(group_name, []).append(username)
            messagebox.showinfo("Info", f"Added {username} to {group_name}")
        else:
            messagebox.showerror("Error", "Invalid username or user already in the group.")

    def get_contact_list(self):
        return [contact for contact in self.users if contact not in ["User1", "User2"]]


    def add_member_to_group(self, group_name, username, window):
        if username and username not in self.group_members.get(group_name, []) and username in self.get_contact_list():
            self.group_members.setdefault(group_name, []).append(username)
            messagebox.showinfo("Info", f"Added {username} to {group_name}")
            self.update_group_listbox()  # Perbarui Listbox setelah menambahkan anggota
        else:
            messagebox.showerror("Error", "Invalid username or user already in the group or not in your contacts.")


    def get_contact_list(self):
        return [contact for contact in self.users if contact not in ["User1", "User2"]]

    def show_group_chat_page(self, group_name):
        if group_name not in self.group_chat_windows:
            self.group_chat_windows[group_name] = ChatWindow(self.root, self, group_name)
        # Remove the following line
        # self.group_chat_windows[group_name].start_chat()


    def show_add_contact_page(self):
        self.add_contact_window = AddContactWindow(self.root, self)

    def show_delete_contact_page(self):
        self.delete_contact_window = DeleteContactWindow(self.root, self, self.add_contact_window)

    def show_setting_page(self):
        if not hasattr(self, 'setting_window') or not self.setting_window or not self.setting_window.winfo_exists():
            self.setting_window = tk.Toplevel(self.root)
            self.setting_window.title("Settings")
            Setting(self.setting_window, self)
            self.setting_window.protocol("WM_DELETE_WINDOW", self.close_setting_page)

    def close_setting_page(self):
        self.setting_window.destroy()
        self.setting_window = None

    def apply_appearance_settings(self):
        theme = self.theme_var.get().lower()
        text_color = self.text_color_var.get().lower()
        font_size = self.font_size_var.get().lower()

        self.apply_settings_to_widget(self.root, theme, text_color, font_size)

        for user, data in self.users.items():
            if data["chat_window"]:
                self.apply_settings_to_widget(data["chat_window"].root, theme, text_color, font_size)

            if self.add_contact_window:
                self.apply_settings_to_widget(self.add_contact_window.add_contact_window, theme, text_color, font_size)

            if self.delete_contact_window:
                self.apply_settings_to_widget(self.delete_contact_window.delete_contact_window, theme, text_color, font_size)

            if self.nav_bar:
                self.apply_settings_to_widget(self.nav_bar, theme, text_color, font_size)

    def apply_settings_to_widget(self, widget, theme, text_color, font_size):
        # Apply theme settings
        widget.configure(bg="black" if theme == "dark" else "white")

        # Apply text color settings
        widget.configure(fg=text_color)

        # Apply font size settings
        widget.configure(font=("Helvetica", 8) if font_size == "small" else
                                  ("Helvetica", 12) if font_size == "medium" else
                                  ("Helvetica", 16))  # Adjust font sizes as needed

    def logout(self):
        # Handle user logout
        if self.nav_bar:
            self.nav_bar.destroy()

        # Reset all data
        self.users = {}
        self.group_chat_windows = {}
        self.group_members = {}
        self.add_contact_window = None
        self.delete_contact_window = None
        self.nav_bar = None
        self.chat_buttons = []
        self.chat_messages = {}

        # Go back to login screen
        self.login_setup()

        # Recreate navigation tabs after logout
        self.create_navigation_tabs(None)
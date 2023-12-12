import tkinter as tk

class GrupChatManager:
    def __init__(self, root, app):
        self.root = root
        self.app = app

        self.groups = []

        self.group_name_var = tk.StringVar()
        self.create_group_window = None

        self.nav_bar = tk.ttk.Notebook(self.root)
        self.nav_bar.pack(fill=tk.BOTH, expand=True)

        self.chat_tab = tk.Frame(self.nav_bar)
        self.nav_bar.add(self.chat_tab, text="Chat")

        # Create other tabs (Contacts, Settings, etc.) here...

        # Add "Groups" tab to the navigation bar
        self.create_group_tab()

    def create_group_tab(self):
        group_frame = tk.Frame(self.nav_bar, bg="lightgray")

        create_group_button = tk.Button(group_frame, text="Create Group", command=self.open_create_group, bg="green", fg="white")
        create_group_button.pack(pady=10)

        self.group_listbox = tk.Listbox(group_frame, selectmode="single", height=10, width=30, bg="white")
        self.group_listbox.pack(padx=10, pady=10)

        self.update_group_listbox()

    def open_create_group(self):
        self.create_group_window = tk.Toplevel(self.root)
        self.create_group_window.title("Create Group")

        self.create_group_view()

    def create_group_view(self):
        group_name_label = tk.Label(self.create_group_window, text="Group Name:")
        group_name_label.pack()

        self.group_name_entry = tk.Entry(self.create_group_window)
        self.group_name_entry.pack()

        add_members_button = tk.Button(self.create_group_window, text="Add Members", command=self.show_add_members_page)
        add_members_button.pack()

        create_button = tk.Button(self.create_group_window, text="Create", command=self.handle_create_group)
        create_button.pack()
        
    def create_group(self):
        group_name = self.group_name_var.get()
        new_group = {"name": group_name, "members": []}
        self.groups.append(new_group)

        self.group_listbox.insert(tk.END, group_name)

        self.create_group_window.destroy()

        self.group_listbox.bind("<Double-Button-1>", lambda event, index=len(self.groups) - 1: self.open_group_chat(event, index))

    def open_group_chat_window(self, group_name):
        if hasattr(self, 'group_chat_windows') and group_name in self.group_chat_windows:
            if self.group_chat_windows[group_name].winfo_exists():
                self.group_chat_windows[group_name].deiconify()
            else:
                del self.group_chat_windows[group_name]
                # Optionally, you may recreate the window here if needed
        else:
            # Create a new chat window if it doesn't exist
            group_chat_window = tk.Toplevel(self.root)
            group_chat_window.title(f"Group Chat - {group_name}")

            chat_window_label = tk.Label(group_chat_window, text=f"Welcome to {group_name} chat!")
            chat_window_label.pack()

            add_member_button = tk.Button(group_chat_window, text="Add Member", command=lambda: self.add_member_to_group(index))
            add_member_button.pack()

            # Store the reference to the chat window
            if not hasattr(self, 'group_chat_windows'):
                self.group_chat_windows = {}
            self.group_chat_windows[group_name] = group_chat_window


    def add_member_to_group(self, index):
        selected_group = self.groups[index]

        add_member_window = tk.Toplevel(self.root)
        add_member_window.title("Add Member")

        contacts = ["Contact 1", "Contact 2", "Contact 3"]  # Placeholder for contacts data

        for contact in contacts:
            contact_checkbox = tk.Checkbutton(add_member_window, text=contact)
            contact_checkbox.pack()

        add_button = tk.Button(add_member_window, text="Add", command=lambda: self.add_selected_members(add_member_window, index))
        add_button.pack()

    def add_selected_members(self, add_member_window, index):
        selected_group = self.groups[index]

        # Logic to add group members from selected contacts
        # Here, you can access the list of selected contacts and add them to the group

        add_member_window.destroy()

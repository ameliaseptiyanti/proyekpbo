from datetime import datetime
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk


class ChatWindow:
    def __init__(self, root, chat_app, username, group_name=None):
        self.root = root
        self.chat_app = chat_app
        self.username = username
        self.message_history = []

        self.message_display = None
        self.message_entry = None
        self.send_button = None
        self.emoji_button = None
        self.image_button = None
        self.add_members_button = None
        self.group_chat = username.startswith("Group")
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(chat_app, username))
        
        



        self.prepare_ui()

    def prepare_ui(self):
        if self.message_display is not None:
            self.message_display.destroy()

        self.message_display = tk.Frame(self.root)
        self.message_display.pack(fill=tk.BOTH, expand=True)

        self.message_entry = tk.Entry(self.root, width=50)
        self.message_entry.pack(pady=10)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack()
        self.send_emoji_button = tk.Button(self.root, text="Send Emoji", command=self.open_emoji_window)
        self.send_emoji_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Example buttons for sending emoji and image

        self.image_button = tk.Button(self.root, text="Send Image", command=self.send_image)
        self.image_button.pack(side=tk.LEFT, padx=5)

        self.add_members_button = None
        if self.group_chat:
            self.add_members_button = tk.Button(self.root, text="Add Members", command=self.show_add_members_page)
            self.add_members_button.pack()

        self.display_messages()

    def display_message(self, user, content, timestamp, anchor_position, profile_color, bubble_color):
        display_text = f"{timestamp} {user}: {content}"

        if not self.message_display.winfo_exists():
            return

        bubble_frame = tk.Frame(self.message_display, bg=bubble_color, bd=2, relief="solid")
        bubble_frame.pack(anchor=anchor_position, padx=5, pady=2, fill=tk.X)

        profile_frame = tk.Frame(bubble_frame)
        profile_frame.pack(side="right" if anchor_position == "w" else "left")
        profile_canvas = tk.Canvas(profile_frame, width=30, height=30, bg="lightgray")
        profile_canvas.create_oval(5, 5, 25, 25, fill=profile_color)
        profile_canvas.pack(padx=5)

        message_label = tk.Label(bubble_frame, text=display_text, font=("Helvetica", 12), bg=bubble_color, fg="black")
        message_label.pack(anchor=anchor_position)

   
 


    def display_image_message(self, user, image_path, timestamp, anchor_position, profile_color, bubble_color):
        display_text = f"{timestamp} {user}: [Image]"

        if not self.message_display.winfo_exists():
            return

        bubble_frame = tk.Frame(self.message_display, bg=bubble_color, bd=2, relief="solid")
        bubble_frame.pack(anchor=anchor_position, padx=5, pady=2, fill=tk.X)

        profile_frame = tk.Frame(bubble_frame)
        profile_frame.pack(side="right" if anchor_position == "w" else "left")
        profile_canvas = tk.Canvas(profile_frame, width=30, height=30, bg="lightgray")
        profile_canvas.create_oval(5, 5, 25, 25, fill=profile_color)
        profile_canvas.pack(padx=5)

        image_label = tk.Label(bubble_frame, text=display_text, font=("Helvetica", 12), bg=bubble_color, fg="black")
        image_label.pack(anchor=anchor_position)

        # Load and display the image
        image = tk.PhotoImage(file=image_path)
        image_label = tk.Label(bubble_frame, image=image, bg=bubble_color)
        image_label.image = image
        image_label.pack(anchor=anchor_position)

    def display_messages(self):
        for widget in self.message_display.winfo_children():
            widget.destroy()

        scrollbar = tk.Scrollbar(self.message_display)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        messages_listbox = tk.Listbox(self.message_display, yscrollcommand=scrollbar.set, selectbackground="lightblue", selectmode="single", bg="white", font=("Helvetica", 12))
        messages_listbox.pack(fill=tk.BOTH, expand=True)

        for user, content, timestamp, message_type, profile_color, bubble_color in self.message_history:
            anchor_position = "w" if user == "You" or self.group_chat else "e"

            if message_type == "text":
                self.display_message(user, content, timestamp, anchor_position, profile_color, bubble_color)
            elif message_type == "emoji":
                self.display_emoji_message(user, content, timestamp, anchor_position, profile_color, bubble_color)

        scrollbar.config(command=messages_listbox.yview)
        
    def display_emoji_message(self, user, emoji, timestamp, anchor_position, profile_color, bubble_color):
        display_text = f"{timestamp} {user}: {emoji}"

        if not self.message_display.winfo_exists():
            return

        bubble_frame = tk.Frame(self.message_display, bg=bubble_color, bd=2, relief="solid")
        bubble_frame.pack(anchor=anchor_position, padx=5, pady=2, fill=tk.X)

        profile_frame = tk.Frame(bubble_frame)
        profile_frame.pack(side="right" if anchor_position == "w" else "left")
        profile_canvas = tk.Canvas(profile_frame, width=30, height=30, bg="lightgray")
        profile_canvas.create_oval(5, 5, 25, 25, fill=profile_color)
        profile_canvas.pack(padx=5)

        message_label = tk.Label(bubble_frame, text=display_text, font=("Helvetica", 12), bg=bubble_color, fg="black")
        message_label.pack(anchor=anchor_position)

    def send_message(self):
        message = self.message_entry.get()
        self.message_entry.delete(0, tk.END)
        timestamp = datetime.now().strftime("%H:%M")
        profile_color = "red" if self.username == "User1" else "yellow"
        bubble_color = "lightblue" if self.username == "User1" else "pink"
        self.message_history.append((self.username, message, timestamp, "text", profile_color, bubble_color))
        self.display_message(self.username, message, timestamp, "w", profile_color, bubble_color)

        if self.group_chat:
            self.chat_app.send_group_message(self.username, message)
        else:
            for user, data in self.chat_app.users.items():
                if user != self.username and data["chat_window"]:
                    data["chat_window"].receive_message(self.username, message, timestamp)
                    
    def open_emoji_window(self):
        emoji_window = tk.Toplevel(self.root)
        emoji_window.title("Select Emoji")

        # Tambahkan emoji-emoji yang ingin ditampilkan dalam daftar
        emojis = ["😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇", "😍", "🥰", "😘", "😗", "😚", "😋", "😛", "😜", "😝", "🤑", "🤗", "🤩", "😎", "🤓", "🧐", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", "😫", "😩", "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "😱", "😨", "😰", "😥", "😓"]

        emoji_listbox = tk.Listbox(emoji_window, selectmode=tk.SINGLE, height=10, width=10, bg="white")
        for emoji in emojis:
            emoji_listbox.insert(tk.END, emoji)
        emoji_listbox.pack(padx=10, pady=10)

        # Tambahkan tombol "Send" untuk mengirim emoji yang dipilih
        send_button = tk.Button(emoji_window, text="Send", command=lambda: self.send_selected_emoji(emoji_listbox))
        send_button.pack(pady=5)
        
    def send_selected_emoji(self, emoji_listbox):
        selected_index = emoji_listbox.curselection()
        if selected_index:
            selected_emoji = emoji_listbox.get(selected_index)
        # Kirim emoji yang dipilih ke pengguna lain (implementasikan sesuai kebutuhan Anda)
        # Anda dapat menggunakan socket atau metode komunikasi lainnya di sini
        # Misalnya: self.send_message(selected_emoji)
        
    def send_selected_emoji(self, emoji_listbox):
        selected_index = emoji_listbox.curselection()
        if selected_index:
            selected_emoji = emoji_listbox.get(selected_index)
            self.send_emoji(selected_emoji)

    def receive_message(self, sender, message, timestamp):
        profile_color = "red" if sender == "User1" else "yellow"
        bubble_color = "lightblue" if sender == "User1" else "pink"
        self.message_history.append((sender, message, timestamp, "text", profile_color, bubble_color))
        self.display_message(sender, message, timestamp, "e", profile_color, bubble_color)

    def send_emoji(self, emoji):
        timestamp = datetime.now().strftime("%H:%M")
        sender = self.username  # Use the current user's username

        # Adjust profile color based on the sender
        profile_color = "red" if sender == "User1" else "yellow"

        # Adjust bubble color based on the sender
        bubble_color = "lightblue" if sender == "User1" else "pink"

        self.message_history.append((sender, emoji, timestamp, "emoji", profile_color, bubble_color))
        self.display_emoji_message(sender, emoji, timestamp, "w", profile_color, bubble_color)

        if self.group_chat:
            self.chat_app.send_group_message(self.username, emoji)
        else:
            for user, data in self.chat_app.users.items():
                if user != self.username and data["chat_window"]:
                    data["chat_window"].receive_emoji(sender, emoji, timestamp, profile_color)

    def receive_emoji(self, sender, emoji, timestamp, sender_profile_color):
        display_text = f"{timestamp} {sender}: {emoji}"

        # Adjust profile color based on the sender
        profile_color = sender_profile_color

        # Adjust bubble color based on the sender
        bubble_color = "lightblue" if sender == "User1" else "pink"

        self.message_history.append((sender, emoji, timestamp, "emoji", profile_color, bubble_color))
        self.display_emoji_message(sender, emoji, timestamp, "e", profile_color, bubble_color)

    def display_messages(self):
           
        for widget in self.message_display.winfo_children():
            widget.destroy()

        scrollbar = tk.Scrollbar(self.message_display)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        messages_listbox = tk.Listbox(self.message_display, yscrollcommand=scrollbar.set, selectbackground="lightblue", selectmode="single", bg="white", font=("Helvetica", 12))
        messages_listbox.pack(fill=tk.BOTH, expand=True)

        for user, content, timestamp, message_type, profile_color, bubble_color in self.message_history:
            anchor_position = "w" if user == "You" or self.group_chat else "e"

            if message_type == "text":
                self.display_message(user, content, timestamp, anchor_position, profile_color, bubble_color)
            elif message_type == "emoji":
                self.display_emoji_message(user, content, timestamp, anchor_position, profile_color, bubble_color)
            elif message_type == "image":
                self.display_image_message(user, content, timestamp, anchor_position, profile_color, bubble_color)

        scrollbar.config(command=messages_listbox.yview)



    def send_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])

        if file_path:
            timestamp = datetime.now().strftime("%H:%M")
            bubble_color = "lightgreen" if self.group_chat else "pink"
            self.message_history.append((self.username, file_path, timestamp, "image", "", bubble_color))
            self.display_image_message(self.username, file_path, timestamp, "w", "", bubble_color)

            # If it's a group chat, send the image to the group members
            if self.group_chat:
                self.chat_app.send_group_message(self.username, file_path, message_type="image")
            else:
                # If it's a one-on-one chat, send the image to the other user
                other_user = [user for user, data in self.chat_app.users.items() if user != self.username and data["chat_window"]]
                if other_user:
                    other_user = other_user[0]
                    self.chat_app.users[other_user]["chat_window"].receive_image(self.username, file_path, timestamp)


    def receive_image(self, sender, image_path, timestamp):
       
        bubble_color = "lightgreen" if self.group_chat else "pink"
        self.message_history.append((sender, image_path, timestamp, "image", "", bubble_color))
        self.display_image_message(sender, image_path, timestamp, "e", "", bubble_color)

    def on_closing(self, chat_app, username):
        # Called when the window is closed
        self.root.destroy()
        # Reset the chat window in the main app
        chat_app.reset_chat(username)




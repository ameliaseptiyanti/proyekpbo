# settings.py
import tkinter as tk
from tkinter import ttk

class Setting(tk.Toplevel):
    def __init__(self, master, chat_app):  # Accept chat_app as an argument
        super().__init__(master)
        self.title("Settings")
        self.geometry("300x200")

        self.chat_app = chat_app

        label = tk.Label(self, text="Appearance Settings", font=("Helvetica", 14))
        label.pack(pady=10)

        # Theme options
        theme_label = tk.Label(self, text="Theme:")
        theme_label.pack(anchor="w", padx=10)
        self.theme_var = tk.StringVar()
        theme_var_options = ["Light", "Dark"]
        theme_combobox = ttk.Combobox(self, textvariable=self.theme_var, values=theme_var_options, state="readonly")
        theme_combobox.set("Light")
        theme_combobox.pack(pady=5)

        # Text color options
        text_color_label = tk.Label(self, text="Text Color:")
        text_color_label.pack(anchor="w", padx=10)
        self.text_color_var = tk.StringVar()
        text_color_var_options = ["Black", "White", "Blue", "Green"]
        text_color_combobox = ttk.Combobox(self, textvariable=self.text_color_var, values=text_color_var_options, state="readonly")
        text_color_combobox.set("Black")
        text_color_combobox.pack(pady=5)

        # Font size options
        font_size_label = tk.Label(self, text="Font Size:")
        font_size_label.pack(anchor="w", padx=10)
        self.font_size_var = tk.StringVar()
        font_size_var_options = ["Small", "Medium", "Large"]
        font_size_combobox = ttk.Combobox(self, textvariable=self.font_size_var, values=font_size_var_options, state="readonly")
        font_size_combobox.set("Medium")
        font_size_combobox.pack(pady=5)

        # Save button
        save_button = tk.Button(self, text="Save", command=self.apply_settings)
        save_button.pack(pady=10)

    def apply_settings(self):
        theme = self.theme_var.get().lower()
        text_color = self.text_color_var.get().lower()
        font_size = self.font_size_var.get().lower()

        # Apply theme settings
        if theme == "dark":
            self.chat_app.root.configure(bg="black")
        else:
            self.chat_app.root.configure(bg="white")

        # Apply text color settings
        # You can modify this to set the color of specific elements in your app
        if text_color == "black":
            pass  # Set text color to black
        elif text_color == "white":
            pass  # Set text color to white
        elif text_color == "blue":
            pass  # Set text color to blue
        elif text_color == "green":
            pass  # Set text color to green

        # Apply font size settings
        # You can modify this to set the font size of specific elements in your app
        if font_size == "small":
            pass  # Set font size to small
        elif font_size == "medium":
            pass  # Set font size to medium
        elif font_size == "large":
            pass  # Set font size to large

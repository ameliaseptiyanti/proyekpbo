# main.py
import tkinter as tk
from chat_app import ChatApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)

    # Modify users after creating the ChatApp instance
    app.users["User1"] = {"password": "pass1", "chat_window": None}
    app.users["User2"] = {"password": "pass2", "chat_window": None}

    root.mainloop()

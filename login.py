import tkinter as tk
from tkinter import messagebox
import os
import subprocess
import sys

USER_FILE = "users.txt"
USER_DIR = "users"

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("PseudoOS Login")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.option_add("*Font", ("Courier New", 18))
        self.build_ui()

    def build_ui(self):
        frame = tk.Frame(self.root, bg="black")
        frame.pack(expand=True)

        title = tk.Label(frame, text="Welcome to PseudoOS", fg="#00FF00", bg="black", font=("Courier New", 30, "bold"))
        title.pack(pady=40)

        self.username_entry = self.create_labeled_entry(frame, "Username:")
        self.password_entry = self.create_labeled_entry(frame, "Password:", show="*")

        button_frame = tk.Frame(frame, bg="black")
        button_frame.pack(pady=30)

        tk.Button(button_frame, text="Login", width=15, command=self.login, bg="black", fg="#00FF00").grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Create Account", width=15, command=self.register, bg="black", fg="#00FF00").grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="Exit", width=15, command=self.root.destroy, bg="black", fg="#00FF00").grid(row=0, column=2, padx=10)

    def create_labeled_entry(self, parent, label, show=None):
        frame = tk.Frame(parent, bg="black")
        frame.pack(pady=10)
        tk.Label(frame, text=label, fg="#00FF00", bg="black").pack(side="left", padx=10)
        entry = tk.Entry(frame, show=show, bg="black", fg="#00FF00", insertbackground="#00FF00")
        entry.pack(side="left", padx=10)
        return entry

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not os.path.exists(USER_FILE):
            messagebox.showerror("Error", "No accounts found. Please create one.")
            return

        with open(USER_FILE, "r") as f:
            for line in f:
                user, pw = line.strip().split("|")
                if username == user and password == pw:
                    messagebox.showinfo("Login Success", f"Welcome back, {username}!")
                    self.launch_desktop(username)
                    return
        messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Username and password cannot be empty.")
            return

        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r") as f:
                for line in f:
                    user, _ = line.strip().split("|")
                    if username == user:
                        messagebox.showerror("Error", "Username already exists.")
                        return

        with open(USER_FILE, "a") as f:
            f.write(f"{username}|{password}\n")

        os.makedirs(os.path.join(USER_DIR, username), exist_ok=True)
        messagebox.showinfo("Success", "Account created! You can now log in.")

    def launch_desktop(self, username):
        desktop_script = os.path.join(os.path.dirname(__file__), "desktop.py")
        python_exec = "python3" if sys.platform != "win32" else "python"
        try:
            subprocess.Popen([python_exec, desktop_script, username])
            # Delay closing login window by 2 seconds
            self.root.after(2000, self.root.destroy)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch desktop: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginScreen(root)
    root.mainloop()
    
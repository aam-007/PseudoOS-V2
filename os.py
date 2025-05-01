import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

class SplashScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Pseudo OS")
        self.master.attributes("-fullscreen", True)
        self.master.configure(bg="black")
        self.master.option_add("*Font", ("Courier New", 20, "bold"))

        content_frame = tk.Frame(self.master, bg="black")
        content_frame.pack(expand=True)

        title_label = tk.Label(
            content_frame,
            text="PSEUDO OS",
            bg="black",
            fg="#00FF00",
            font=("Courier New", 36, "bold")
        )
        title_label.pack(pady=(0, 50))

        button_frame = tk.Frame(content_frame, bg="black")
        button_frame.pack()

        boot_button = tk.Button(
            button_frame,
            text="Boot Pseudo OS",
            width=20,
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.boot_os
        )
        boot_button.pack(pady=20)

        about_button = tk.Button(
            button_frame,
            text="About",
            width=20,
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.show_about
        )
        about_button.pack(pady=20)

        exit_button = tk.Button(
            button_frame,
            text="Exit",
            width=20,
            height=2,
            bg="black",
            fg="#00FF00",
            activebackground="gray",
            activeforeground="white",
            command=self.exit_app
        )
        exit_button.pack(pady=20)

    def boot_os(self):
        # Launch boot.py asynchronously
        subprocess.Popen([sys.executable, "boot.py"])
        # Exit this screen after 2 seconds
        self.master.after(2000, lambda: exit(0))

    def show_about(self):
        messagebox.showinfo("About", "Pseudo OS\nVersion 2.0\nDeveloped by PhonexLegend")

    def exit_app(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SplashScreen(root)
    root.mainloop()

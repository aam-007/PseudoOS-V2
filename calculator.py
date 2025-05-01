import tkinter as tk
from tkinter import messagebox
import math
import time
import os
import sys

class Calculator:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.history = []
        self.user_dir = os.path.join("users", self.username, "calc")
        os.makedirs(self.user_dir, exist_ok=True)
        self.history_file = os.path.join(self.user_dir, "history.txt")

        self.root.title("PseudoOS Calculator")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Key>", self.key_input)

        self.expression = ""
        self.build_ui()
        self.update_clock()

    def build_ui(self):
        self.clock_label = tk.Label(self.root, font=("Courier New", 14), fg="#00FF00", bg="black")
        self.clock_label.pack(pady=10)

        self.display = tk.Entry(self.root, font=("Courier New", 24), bg="black", fg="#00FF00",
                                insertbackground="#00FF00", justify="right")
        self.display.pack(fill="x", padx=10, pady=20)

        btn_rows = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '=', '+'],
            ['(', ')', '^', '%'],
            ['π', 'e', 'sqrt', 'mod'],
        ]

        for row in btn_rows:
            frame = tk.Frame(self.root, bg="black")
            frame.pack()
            for char in row:
                btn = tk.Button(frame, text=char, font=("Courier New", 16), width=5, height=2,
                                fg="#00FF00", bg="black", activebackground="#111", activeforeground="#00FF00",
                                command=lambda c=char: self.button_press(c))
                btn.pack(side="left", padx=5, pady=5)

        extra = tk.Frame(self.root, bg="black")
        extra.pack(pady=10)
        tk.Button(extra, text="Clear", command=self.clear, fg="#00FF00", bg="black").pack(side="left", padx=5)
        tk.Button(extra, text="Delete History", command=self.delete_history, fg="#00FF00", bg="black").pack(side="left", padx=5)
        tk.Button(extra, text="Exit", command=self.root.destroy, fg="#00FF00", bg="black").pack(side="left", padx=5)

        self.history_box = tk.Text(self.root, height=10, bg="black", fg="#00FF00", font=("Courier New", 12))
        self.history_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.history_box.config(state="disabled")

        self.load_history()

    def update_clock(self):
        current_time = time.strftime("%a, %Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)

    def button_press(self, char):
        if char == "=":
            self.calculate()
        elif char == "π":
            self.expression += str(math.pi)
        elif char == "e":
            self.expression += str(math.e)
        elif char == "sqrt":
            self.expression += "math.sqrt("
        elif char == "^":
            self.expression += "**"
        elif char == "mod":
            self.expression += "%"
        else:
            self.expression += char

        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def key_input(self, event):
        key = event.char
        if key in '0123456789.+-*/()%':
            self.expression += key
        elif key == '\r':
            self.calculate()
            return
        elif key == '\x08':  # Backspace
            self.expression = self.expression[:-1]
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def calculate(self):
        try:
            result = str(eval(self.expression))
            timestamp = time.strftime("%a %Y-%m-%d %H:%M:%S")
            entry = f"{timestamp}: {self.expression} = {result}"
            self.history.append(entry)
            self.save_history(entry)
            self.update_history_box(entry)
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, result)
            self.expression = ""
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Expression\n\n{e}")
            self.expression = ""

    def clear(self):
        self.expression = ""
        self.display.delete(0, tk.END)

    def save_history(self, entry):
        with open(self.history_file, "a") as f:
            f.write(entry + "\n")

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, "r") as f:
                self.history = f.read().splitlines()
            for entry in self.history:
                self.update_history_box(entry)

    def update_history_box(self, entry):
        self.history_box.config(state="normal")
        self.history_box.insert(tk.END, entry + "\n")
        self.history_box.config(state="disabled")

    def delete_history(self):
        if messagebox.askyesno("Delete", "Are you sure you want to delete all history?"):
            self.history = []
            if os.path.exists(self.history_file):
                os.remove(self.history_file)
            self.history_box.config(state="normal")
            self.history_box.delete("1.0", tk.END)
            self.history_box.config(state="disabled")
            messagebox.showinfo("Deleted", "History cleared.")

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = Calculator(root, username)
    root.mainloop()

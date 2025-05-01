import tkinter as tk
from tkinter import messagebox
import os
import sys
import time
import subprocess

class Terminal:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        # Sandbox to user’s folder
        self.base_dir = os.path.abspath(os.path.join("users", self.username))
        self.current_dir = self.base_dir

        self.root.title("PseudoOS Terminal")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.option_add("*Font", ("Courier New", 14))

        # Output area
        self.output = tk.Text(self.root, bg="black", fg="#00FF00",
                              insertbackground="#00FF00", wrap="word")
        self.output.pack(fill="both", expand=True)
        self.output.config(state="disabled")

        # Input area
        self.input_entry = tk.Entry(self.root, bg="black", fg="#00FF00",
                                    insertbackground="#00FF00")
        self.input_entry.pack(fill="x")
        self.input_entry.bind("<Return>", self.process_command)
        self.input_entry.focus_set()

        # On launch: show help then prompt
        self.show_commands()
        self.print_prompt()

    def show_commands(self):
        help_text = (
            "Available commands:\n"
            "  cd [dir]           – Change directory (to Home if omitted)\n"
            "  ls                 – List items in current directory\n"
            "  tree               – Recursively list directory structure\n"
            "  pwd                – Print working directory\n"
            "  mkdir <name>       – Create a new folder\n"
            "  rmdir <name>       – Remove an empty folder\n"
            "  rm <file>          – Delete a file\n"
            "  touch <file>       – Create an empty file\n"
            "  cp <src> <dst>     – Copy files\n"
            "  mv <src> <dst>     – Move or rename files\n"
            "  cat <file>         – Display file contents\n"
            "  clear              – Clear the terminal screen\n"
            "  whoami             – Show current user\n"
            "  date               – Show current date & time\n"
            "  grep <pat> <file>  – Search for pattern in file\n"
            "  notes <file.txt>   – Open a text file in Notes app\n"
            "  exit               – Close the terminal\n\n"
        )
        self.write_output(help_text)

    def print_prompt(self):
        rel = os.path.relpath(self.current_dir, self.base_dir)
        if rel == ".":
            rel = "Home"
        else:
            rel = "Home/" + rel
        prompt = f"{rel}> "
        self.write_output(prompt, end="")
        self.input_entry.delete(0, tk.END)
        self.input_entry.focus_set()

    def process_command(self, event):
        cmd_line = self.input_entry.get().strip()
        self.write_output(cmd_line + "\n")
        self.execute_command(cmd_line)
        self.print_prompt()

    def execute_command(self, command):
        if not command:
            return
        parts = command.split()
        cmd, args = parts[0], parts[1:]
        if cmd == "cd":
            self.change_directory(args)
        elif cmd == "ls":
            self.list_directory()
        elif cmd == "tree":
            self.tree_directory()
        elif cmd == "pwd":
            self.write_output(self.current_dir + "\n")
        elif cmd == "mkdir":
            self.mkdir(args)
        elif cmd == "rmdir":
            self.rmdir(args)
        elif cmd == "rm":
            self.rm(args)
        elif cmd == "touch":
            self.touch(args)
        elif cmd == "cp":
            self.cp(args)
        elif cmd == "mv":
            self.mv(args)
        elif cmd == "cat":
            self.cat(args)
        elif cmd == "clear":
            self.output.config(state="normal")
            self.output.delete("1.0", tk.END)
            self.output.config(state="disabled")
        elif cmd == "whoami":
            self.write_output(self.username + "\n")
        elif cmd == "date":
            self.write_output(time.strftime("%A, %d %B %Y | %H:%M:%S") + "\n")
        elif cmd == "grep":
            self.grep(args)
        elif cmd == "notes":
            self.notes(args)
        elif cmd == "exit":
            self.root.destroy()
        else:
            self.write_output("Unknown command\n")

    def change_directory(self, args):
        target = self.base_dir if not args else os.path.join(self.current_dir, args[0])
        abs_t = os.path.abspath(target)
        if abs_t.startswith(self.base_dir) and os.path.isdir(abs_t):
            self.current_dir = abs_t
        else:
            self.write_output("Access Denied or Directory not found\n")

    def list_directory(self):
        try:
            for item in sorted(os.listdir(self.current_dir)):
                self.write_output(item + "\n")
        except Exception as e:
            self.write_output(f"Error: {e}\n")

    def tree_directory(self):
        def rec(p, indent=""):
            for i in sorted(os.listdir(p)):
                full = os.path.join(p, i)
                self.write_output(indent + i + "\n")
                if os.path.isdir(full):
                    rec(full, indent + "    ")
        rec(self.current_dir)

    def mkdir(self, args):
        if not args:
            self.write_output("Usage: mkdir <folder>\n")
            return
        path = os.path.abspath(os.path.join(self.current_dir, args[0]))
        if path.startswith(self.base_dir):
            try:
                os.makedirs(path, exist_ok=False)
            except Exception as e:
                self.write_output(f"Error: {e}\n")

    def rmdir(self, args):
        if not args:
            self.write_output("Usage: rmdir <folder>\n")
            return
        path = os.path.abspath(os.path.join(self.current_dir, args[0]))
        if path.startswith(self.base_dir) and os.path.isdir(path):
            try:
                os.rmdir(path)
            except Exception as e:
                self.write_output(f"Error: {e}\n")

    def rm(self, args):
        if not args:
            self.write_output("Usage: rm <file>\n")
            return
        path = os.path.abspath(os.path.join(self.current_dir, args[0]))
        if path.startswith(self.base_dir) and os.path.isfile(path):
            try:
                os.remove(path)
            except Exception as e:
                self.write_output(f"Error: {e}\n")

    def touch(self, args):
        if not args:
            self.write_output("Usage: touch <file>\n")
            return
        path = os.path.abspath(os.path.join(self.current_dir, args[0]))
        if path.startswith(self.base_dir):
            open(path, "a").close()

    def cp(self, args):
        if len(args) != 2:
            self.write_output("Usage: cp <src> <dst>\n")
            return
        src = os.path.abspath(os.path.join(self.current_dir, args[0]))
        dst = os.path.abspath(os.path.join(self.current_dir, args[1]))
        if src.startswith(self.base_dir) and dst.startswith(self.base_dir):
            try:
                import shutil; shutil.copy(src, dst)
            except Exception as e:
                self.write_output(f"Error: {e}\n")

    def mv(self, args):
        if len(args) != 2:
            self.write_output("Usage: mv <src> <dst>\n")
            return
        src = os.path.abspath(os.path.join(self.current_dir, args[0]))
        dst = os.path.abspath(os.path.join(self.current_dir, args[1]))
        if src.startswith(self.base_dir) and dst.startswith(self.base_dir):
            try:
                os.rename(src, dst)
            except Exception as e:
                self.write_output(f"Error: {e}\n")

    def cat(self, args):
        if not args:
            self.write_output("Usage: cat <file>\n")
            return
        path = os.path.abspath(os.path.join(self.current_dir, args[0]))
        if path.startswith(self.base_dir) and os.path.isfile(path):
            with open(path) as f:
                self.write_output(f.read() + "\n")

    def grep(self, args):
        if len(args) != 2:
            self.write_output("Usage: grep <pattern> <file>\n")
            return
        pat, fname = args
        path = os.path.abspath(os.path.join(self.current_dir, fname))
        if path.startswith(self.base_dir) and os.path.isfile(path):
            for line in open(path):
                if pat in line:
                    self.write_output(line)

    def notes(self, args):
        if not args:
            self.write_output("Usage: notes <file.txt>\n")
            return
        fname = args[0]
        path = os.path.abspath(os.path.join(self.current_dir, fname))
        if path.startswith(self.base_dir) and path.endswith(".txt") and os.path.isfile(path):
            subprocess.Popen(["python3", "notes.py", self.username, path])
        else:
            self.write_output("Error: invalid or missing file\n")

    def write_output(self, text, end="\n"):
        self.output.config(state="normal")
        self.output.insert(tk.END, text if end=="" else text)
        if end == "":
            # already included
            pass
        self.output.config(state="disabled")
        self.output.see(tk.END)

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = Terminal(root, username)
    root.mainloop()

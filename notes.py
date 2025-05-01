import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import time

class NotesApp:
    def __init__(self, root, username, file_path=None):
        self.root = root
        self.username = username
        # Set base directory to the user's folder (sandbox)
        self.user_base = os.path.abspath(os.path.join("users", self.username))
        # For notes, we allow saving anywhere inside the user's folder
        self.user_notes_dir = os.path.join(self.user_base, "notes")
        os.makedirs(self.user_notes_dir, exist_ok=True)
        
        # If a file path is passed, verify it's within the user's folder
        if file_path:
            abs_file = os.path.abspath(file_path)
            if abs_file.startswith(self.user_base):
                self.current_file = abs_file
            else:
                messagebox.showerror("Access Denied", "You can only open files within your own user folder.")
                self.current_file = None
        else:
            self.current_file = None

        self.root.title("PseudoOS Notes")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.build_ui()

        if self.current_file:
            self.load_file()

    def build_ui(self):
        self.text_area = tk.Text(self.root, wrap="word", bg="black", fg="#00FF00",
                                 insertbackground="#00FF00", font=("Courier New", 14))
        self.text_area.pack(expand=True, fill="both", padx=10, pady=10)

        btn_frame = tk.Frame(self.root, bg="black")
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="New", command=self.new_file,
                  bg="black", fg="#00FF00", font=("Courier New", 12), width=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Open", command=self.open_file_dialog,
                  bg="black", fg="#00FF00", font=("Courier New", 12), width=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Save", command=self.save_file,
                  bg="black", fg="#00FF00", font=("Courier New", 12), width=10).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Exit", command=self.root.destroy,
                  bg="black", fg="#00FF00", font=("Courier New", 12), width=10).pack(side="right", padx=10)

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.current_file = None

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(
            initialdir=self.user_base,
            title="Open Note",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            abs_file = os.path.abspath(file_path)
            if abs_file.startswith(self.user_base):
                self.current_file = abs_file
                self.load_file()
            else:
                messagebox.showerror("Access Denied", "You can only open files within your own user folder.")

    def load_file(self):
        if self.current_file and os.path.exists(self.current_file):
            try:
                with open(self.current_file, "r", encoding="utf-8") as f:
                    content = f.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, content)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load file:\n{e}")
        else:
            messagebox.showwarning("Warning", "File not found or inaccessible.")

    def save_file(self):
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self.save_file_as()

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(
            initialdir=self.user_base,
            title="Save Note As",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            abs_file = os.path.abspath(file_path)
            if abs_file.startswith(self.user_base):
                self.current_file = abs_file
                self._save_to_file(abs_file)
            else:
                messagebox.showerror("Access Denied", "You can only save files in your own user folder.")

    def _save_to_file(self, path):
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(self.text_area.get("1.0", tk.END))
            # Optionally, update title with a save confirmation message
            self.root.title(f"PseudoOS Notes - Saved at {time.strftime('[%H:%M:%S]')}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file:\n{e}")

if __name__ == "__main__":
    # Username is required as first argument; optional file path as second argument.
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    file_path = sys.argv[2] if len(sys.argv) > 2 else None

    root = tk.Tk()
    app = NotesApp(root, username, file_path)
    root.mainloop()

import tkinter as tk
import os
import subprocess
import sys
from datetime import datetime

class Desktop:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title(f"PseudoOS - {self.username}")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")
        self.root.option_add("*Font", ("Courier New", 14))

        self.user_dir = os.path.join("users", self.username)
        os.makedirs(self.user_dir, exist_ok=True)

        self.create_desktop_icons()
        self.create_taskbar()
        self.update_clock()

    def create_desktop_icons(self):
        icon_frame = tk.Frame(self.root, bg="black")
        icon_frame.pack(side="top", anchor="nw", padx=50, pady=30)

        self.create_icon(icon_frame, "My Computer", self.launch_my_computer)
        self.create_icon(icon_frame, "Calculator", self.launch_calculator)
        self.create_icon(icon_frame, "Terminal", self.launch_terminal)
        self.create_icon(icon_frame, "Notes", self.launch_notes)
        self.create_icon(icon_frame, "Snake Game", self.launch_snake)
        self.create_icon(icon_frame, "Pong Game", self.launch_pong)
        self.create_icon(icon_frame, "Tetris", self.launch_tetris)
        self.create_icon(icon_frame, "Path Finder", self.launch_pathfinder)
        self.create_icon(icon_frame, "Maze", self.launch_maze)  # NEW LINE

    def create_icon(self, parent, name, command):
        btn = tk.Button(parent, text=name, width=20, height=2, 
                      bg="black", fg="#00FF00", activebackground="black",
                      activeforeground="#00FF00", command=command)
        btn.pack(anchor="w", pady=10)

    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg="black")
        self.taskbar.pack(side="bottom", fill="x")

        self.shutdown_btn = tk.Button(self.taskbar, text="Shutdown", 
                                    command=self.shutdown, bg="black",
                                    fg="#00FF00", activebackground="black",
                                    activeforeground="#00FF00")
        self.shutdown_btn.pack(side="left", padx=10, pady=5)

        self.clock_label = tk.Label(self.taskbar, fg="#00FF00", bg="black")
        self.clock_label.pack(side="right", padx=10)

    def update_clock(self):
        now = datetime.now()
        time_str = now.strftime("%A, %d %B %Y | %H:%M:%S")
        self.clock_label.config(text=time_str)
        self.root.after(1000, self.update_clock)

    def launch_script(self, script_name):
        script_path = os.path.join(os.path.dirname(__file__), script_name)
        python_exec = "python3" if sys.platform != "win32" else "python"
        subprocess.Popen([python_exec, script_path, self.username])

    def launch_my_computer(self): self.launch_script("my_computer.py")
    def launch_calculator(self): self.launch_script("calculator.py")
    def launch_terminal(self): self.launch_script("terminal.py")
    def launch_notes(self): self.launch_script("notes.py")
    def launch_snake(self): self.launch_script("snake.py")
    def launch_pong(self): self.launch_script("pong.py")
    def launch_tetris(self): self.launch_script("tetris.py")
    def launch_pathfinder(self): self.launch_script("pathfinder.py")
    def launch_maze(self): self.launch_script("maze.py")  # NEW LINE

    def shutdown(self):
        shutdown_script = os.path.join(os.path.dirname(__file__), "shutdown.py")
        python_exec = "python3" if sys.platform != "win32" else "python"
        try:
            subprocess.Popen([python_exec, shutdown_script])
            self.root.after(2000, lambda: os._exit(0))
        except Exception as e:
            print(f"Shutdown failed: {e}")

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = Desktop(root, username)
    root.mainloop()

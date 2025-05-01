import tkinter as tk
import time
import threading
import subprocess
import sys
import os

class BootScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Booting PseudoOS")
        self.root.configure(bg="black")
        self.root.attributes("-fullscreen", True)

        self.text_area = tk.Text(
            self.root,
            bg="black",
            fg="#00FF00",
            font=("Courier New", 24),
            borderwidth=0,
            highlightthickness=0
        )
        self.text_area.pack(expand=True, fill="both")
        self.text_area.config(state=tk.DISABLED)

        threading.Thread(target=self.boot_sequence).start()

    def print_line(self, text, delay=0.4):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text + "\n")
        self.text_area.see(tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.root.update()
        time.sleep(delay)

    def boot_sequence(self):
        boot_lines = [
            "[   OK   ] Initializing BIOS...",
            "[   OK   ] Detecting hardware components...",
            "[   OK   ] CPU: PseudoCore v1.3 @ 2.6GHz",
            "[   OK   ] RAM: 2048MB Virtual SDRAM",
            "[   OK   ] VGA Display: 800x600@60Hz",
            "[   OK   ] Keyboard and Mouse detected",
            "[   OK   ] Loading Pseudo Kernel...",
            "[   OK   ] Mounting /pseudo/root",
            "[   OK   ] Mounting /home/user",
            "[   OK   ] Establishing loopback interface",
            "[   OK   ] Pseudo Network: connected (192.168.0.42)",
            "[   OK   ] Loading Pseudo Drivers...",
            "[   OK   ] Starting system services",
            "[   OK   ] Launching GUI Shell",
            "[ SYSTEM ] Welcome to PseudoOS.",
            "[ SYSTEM ] Type 'help' to get started.",
        ]

        for line in boot_lines:
            self.print_line(line)

        # Launch login.py first
        login_script = os.path.join(os.path.dirname(__file__), "login.py")
        python_exec = "python3" if sys.platform != "win32" else "python"

        try:
            subprocess.Popen([python_exec, login_script])
            self.root.after(500, self.root.destroy)  # Delayed close
        except Exception as e:
            print(f"[ERROR] Failed to launch login.py: {e}")
            time.sleep(5)

if __name__ == "__main__":
    root = tk.Tk()
    app = BootScreen(root)
    root.mainloop()

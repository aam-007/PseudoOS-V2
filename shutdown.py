import tkinter as tk
import time
import os
import sys
import signal
import platform

class ShutdownScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Shutting Down")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.label = tk.Label(self.root, text="System Shutting Down...",
                              font=("Courier New", 32), fg="#00FF00", bg="black")
        self.label.pack(pady=100)

        self.text = tk.Text(self.root, font=("Courier New", 14),
                            bg="black", fg="#00FF00", height=25, width=100, bd=0)
        self.text.pack()
        self.text.configure(state="disabled")

        self.shutdown_sequence()

    def shutdown_sequence(self):
        messages = [
            "[ OK ] Closing active applications...",
            "[ OK ] Sending shutdown signals...",
            "[ OK ] Saving user session...",
            "[ OK ] Unmounting virtual drives...",
            "[ OK ] Disconnecting peripherals...",
            "[ OK ] Terminating session handlers...",
            "[ OK ] Killing orphan processes...",
            "[ OK ] Writing system logs...",
            "[ OK ] Stopping background daemons...",
            "[ OK ] Releasing memory buffers...",
            "[ OK ] Cleaning up temporary files...",
            "[ OK ] Disabling user input...",
            "[ OK ] Flushing DNS cache...",
            "[ OK ] Terminating display server...",
            "[ OK ] Logging out...",
            "[ OK ] Powering down network interfaces...",
            "[ OK ] Resetting hardware states...",
            "[ OK ] Halting kernel modules...",
            "[ OK ] Shutting down power management...",
            "[ OK ] Stopping clock daemon...",
            "[ OK ] Syncing system time...",
            "[ OK ] De-initializing device tree...",
            "[ OK ] Finalizing shutdown tasks...",
            "[ OK ] Compressing memory swap...",
            "[ OK ] Power circuits disengaged...",
            "[ OK ] CPU halted...",
            "[ OK ] PseudoOS safely halted."
        ]

        def show_next(index=0):
            if index < len(messages):
                self.text.configure(state="normal")
                self.text.insert(tk.END, messages[index] + "\n")
                self.text.see(tk.END)
                self.text.configure(state="disabled")
                self.root.after(300, show_next, index + 1)
            else:
                self.terminate()

        show_next()

    def terminate(self):
        self.root.destroy()
        time.sleep(0.5)

        # Cross-platform force exit
        if platform.system() == "Windows":
            os.system("taskkill /F /PID " + str(os.getpid()))
        else:
            os.kill(os.getpid(), signal.SIGTERM)


if __name__ == "__main__":
    root = tk.Tk()
    app = ShutdownScreen(root)
    root.mainloop()

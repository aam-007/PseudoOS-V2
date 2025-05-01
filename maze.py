import tkinter as tk
import math
from datetime import datetime

class RetroExplorer(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, bg='black', highlightthickness=0)
        self.pack(fill='both', expand=True)

        self.master = master  # Keep reference for closing
        self.map_size = 16
        self.pos_x, self.pos_y = 1.5, 1.5
        self.dir_x, self.dir_y = 1, 0
        self.plane_x, self.plane_y = 0, 0.66

        # Simple 16x16 map
        self.map = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1],
            [1,0,1,0,1,1,1,1,1,1,1,1,0,1,0,1],
            [1,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
            [1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1],
            [1,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,0,0,1,1,1,1,1,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ]

        self.move_speed = 0.2
        self.rot_speed = 0.1
        self.keys = {'Up': False, 'Down': False, 'Left': False, 'Right': False}

        # UI Top Bar (Clock + Exit)
        self.ui_frame = tk.Frame(master, bg="black")
        self.ui_frame.place(relx=0, rely=0, anchor='nw')

        self.clock_label = tk.Label(self.ui_frame, text="", fg="#00FF00", bg="black", font=("Courier New", 14))
        self.clock_label.pack(side="left", padx=20, pady=5)

        self.exit_btn = tk.Button(self.ui_frame, text="Exit to Desktop", command=self.exit_to_desktop,
                                  fg="#00FF00", bg="black", activebackground="black",
                                  activeforeground="#00FF00", font=("Courier New", 12))
        self.exit_btn.pack(side="right", padx=20)

        self.bind_all('<KeyPress>', self.key_press)
        self.bind_all('<KeyRelease>', self.key_release)
        self.focus_set()

        self.update_clock()
        self.game_loop()

    def update_clock(self):
        now = datetime.now()
        self.clock_label.config(text=now.strftime("%A, %d %B %Y | %H:%M:%S"))
        self.master.after(1000, self.update_clock)

    def exit_to_desktop(self):
        self.master.destroy()

    def key_press(self, e):
        if e.keysym in self.keys:
            self.keys[e.keysym] = True

    def key_release(self, e):
        if e.keysym in self.keys:
            self.keys[e.keysym] = False

    def move_player(self):
        if self.keys['Up']:
            new_x = self.pos_x + self.dir_x * self.move_speed
            new_y = self.pos_y + self.dir_y * self.move_speed
            if self.is_valid_position(new_x, new_y):
                self.pos_x, self.pos_y = new_x, new_y

        if self.keys['Down']:
            new_x = self.pos_x - self.dir_x * self.move_speed
            new_y = self.pos_y - self.dir_y * self.move_speed
            if self.is_valid_position(new_x, new_y):
                self.pos_x, self.pos_y = new_x, new_y

        if self.keys['Left']:
            self.rotate(self.rot_speed)
        if self.keys['Right']:
            self.rotate(-self.rot_speed)

    def is_valid_position(self, x, y):
        return (0 <= x < self.map_size and 0 <= y < self.map_size and self.map[int(x)][int(y)] == 0)

    def rotate(self, angle):
        cos = math.cos(angle)
        sin = math.sin(angle)
        old_dir_x = self.dir_x
        self.dir_x = old_dir_x * cos - self.dir_y * sin
        self.dir_y = old_dir_x * sin + self.dir_y * cos
        old_plane_x = self.plane_x
        self.plane_x = old_plane_x * cos - self.plane_y * sin
        self.plane_y = old_plane_x * sin + self.plane_y * cos

    def raycast(self):
        w, h = self.winfo_width(), self.winfo_height()
        for x in range(w // 2):
            camera_x = 2 * x / (w // 2) - 1
            ray_dir_x = self.dir_x + self.plane_x * camera_x
            ray_dir_y = self.dir_y + self.plane_y * camera_x

            map_x, map_y = int(self.pos_x), int(self.pos_y)
            delta_dist_x = abs(1 / ray_dir_x) if ray_dir_x else 1e30
            delta_dist_y = abs(1 / ray_dir_y) if ray_dir_y else 1e30

            step_x = 1 if ray_dir_x < 0 else -1
            side_dist_x = (self.pos_x - map_x) * delta_dist_x if ray_dir_x < 0 else (map_x + 1 - self.pos_x) * delta_dist_x
            step_y = 1 if ray_dir_y < 0 else -1
            side_dist_y = (self.pos_y - map_y) * delta_dist_y if ray_dir_y < 0 else (map_y + 1 - self.pos_y) * delta_dist_y

            hit = False
            side = 0
            while not hit:
                if side_dist_x < side_dist_y:
                    side_dist_x += delta_dist_x
                    map_x += step_x
                    side = 0
                else:
                    side_dist_y += delta_dist_y
                    map_y += step_y
                    side = 1

                if 0 <= map_x < self.map_size and 0 <= map_y < self.map_size:
                    if self.map[map_x][map_y] > 0:
                        hit = True
                else:
                    break

            if hit:
                perp_wall_dist = (map_x - self.pos_x + (1 - step_x)/2) / ray_dir_x if side == 0 else (map_y - self.pos_y + (1 - step_y)/2) / ray_dir_y
                line_height = int(h / (perp_wall_dist + 0.0001))
                color = "#002200" if side == 1 else "#004400"
                self.create_line(x*2, h//2 - line_height//2, x*2, h//2 + line_height//2, fill=color, width=2)

    def draw_hud(self):
        w, h = self.winfo_width(), self.winfo_height()
        self.create_oval(w//2-5, h//2-5, w//2+5, h//2+5, outline="#00FF00")

    def game_loop(self):
        self.delete('all')
        self.move_player()
        self.raycast()
        self.draw_hud()
        self.after(50, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")
    game = RetroExplorer(root)
    root.mainloop()

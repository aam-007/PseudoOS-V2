import tkinter as tk
import random
import time


class InfiniteTetris:
    def __init__(self, root):
        self.root = root
        self.root.title("∞ Infinite Tetris ∞")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.cell_size = 30
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.grid_cols = 10
        self.grid_rows = 30
        self.offset_x = (self.width - self.grid_cols * self.cell_size) // 2
        self.offset_y = (self.height - self.grid_rows * self.cell_size) // 2

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.grid = [[0] * self.grid_cols for _ in range(self.grid_rows)]
        self.current_piece = None
        self.current_pos = None
        self.running = False
        self.paused = False
        self.start_time = None
        self.pause_time = 0
        self.pause_start = None

        self.shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[1, 1, 1], [0, 1, 0]],  # T
            [[1, 1, 1], [1, 0, 0]],  # L
            [[1, 1, 1], [0, 0, 1]],  # J
            [[1, 1, 0], [0, 1, 1]],  # S
            [[0, 1, 1], [1, 1, 0]]   # Z
        ]
        self.colors = ["cyan", "yellow", "purple", "orange", "blue", "green", "red"]

        self.blink = True
        self.show_splash_screen()

    def show_splash_screen(self):
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width // 2,
            self.height // 2 - 60,
            text="∞  I N F I N I T E   T E T R I S  ∞",
            font=("Courier New", 48, "bold"),
            fill="#00FF00"
        )

        self.splash_blink_text = self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="Press any key to begin",
            font=("Courier New", 20),
            fill="#00FF00"
        )

        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 40,
            text="← → to move | ↑ to rotate | ↓ to drop | P to pause | Q to exit",
            font=("Courier New", 14),
            fill="#00FF00"
        )

        self.blink_text()
        self.root.bind("<Key>", self.start_game)

    def blink_text(self):
        if self.blink:
            self.canvas.itemconfigure(self.splash_blink_text, state='hidden')
        else:
            self.canvas.itemconfigure(self.splash_blink_text, state='normal')
        self.blink = not self.blink
        self.root.after(500, self.blink_text)

    def start_game(self, event=None):
        self.root.unbind("<Key>")
        self.root.bind("<KeyPress>", self.handle_key)
        self.canvas.delete("all")
        self.running = True
        self.paused = False
        self.start_time = time.time()
        self.pause_time = 0
        self.grid = [[0] * self.grid_cols for _ in range(self.grid_rows)]
        self.spawn_piece()
        self.game_loop()

    def spawn_piece(self):
        idx = random.randint(0, len(self.shapes)-1)
        self.current_piece = self.shapes[idx]
        self.current_color = self.colors[idx]
        self.current_pos = [self.grid_cols // 2 - len(self.current_piece[0]) // 2, 0]
        if self.check_collision(self.current_pos[0], self.current_pos[1], self.current_piece):
            self.clear_grid()

    def check_collision(self, x, y, piece):
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                if piece[row][col]:
                    grid_x = x + col
                    grid_y = y + row
                    if (grid_x < 0 or grid_x >= self.grid_cols or
                        grid_y >= self.grid_rows or
                        (grid_y >= 0 and self.grid[grid_y][grid_x])):
                        return True
        return False

    def move_piece(self, dx, dy):
        new_x = self.current_pos[0] + dx
        new_y = self.current_pos[1] + dy
        if not self.check_collision(new_x, new_y, self.current_piece):
            self.current_pos = [new_x, new_y]
            return True
        return False

    def rotate_piece(self):
        rotated = list(zip(*reversed(self.current_piece)))
        if not self.check_collision(self.current_pos[0], self.current_pos[1], rotated):
            self.current_piece = rotated

    def merge_piece(self):
        for row in range(len(self.current_piece)):
            for col in range(len(self.current_piece[row])):
                if self.current_piece[row][col]:
                    grid_x = self.current_pos[0] + col
                    grid_y = self.current_pos[1] + row
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = self.current_color

    def clear_lines(self):
        new_grid = []
        for row in self.grid:
            if 0 not in row:
                continue
            new_grid.append(row)
        while len(new_grid) < self.grid_rows:
            new_grid.insert(0, [0] * self.grid_cols)
        self.grid = new_grid

    def clear_grid(self):
        self.grid = [[0] * self.grid_cols for _ in range(self.grid_rows)]

    def game_loop(self):
        if not self.running or self.paused:
            return

        if not self.move_piece(0, 1):
            self.merge_piece()
            self.clear_lines()
            self.spawn_piece()

        self.draw()
        self.root.after(100, self.game_loop)

    def draw(self):
        self.canvas.delete("all")

        for y in range(self.grid_rows):
            for x in range(self.grid_cols):
                if self.grid[y][x]:
                    self.draw_block(x, y, self.grid[y][x])

        if self.current_piece:
            for y in range(len(self.current_piece)):
                for x in range(len(self.current_piece[y])):
                    if self.current_piece[y][x]:
                        px = self.current_pos[0] + x
                        py = self.current_pos[1] + y
                        if py >= 0:
                            self.draw_block(px, py, self.current_color)

        x0 = self.offset_x
        y0 = self.offset_y
        x1 = x0 + self.grid_cols * self.cell_size
        y1 = y0 + self.grid_rows * self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="white", width=2)

        elapsed = int(time.time() - self.start_time - self.pause_time)
        mins = elapsed // 60
        secs = elapsed % 60
        current_time = time.strftime("%A, %d %B %Y | %H:%M:%S")

        info_text = (
            f"⏱ Elapsed: {mins}m {secs}s\n"
            f"{current_time}"
        )
        self.canvas.create_text(
            self.width - 250,
            50,
            text=info_text,
            anchor="ne",
            fill="#00FF00",
            font=("Courier New", 14)
        )

        if self.paused:
            self.canvas.create_text(
                self.width // 2,
                self.height // 2,
                text="⏸ PAUSED",
                fill="#FFFF00",
                font=("Courier New", 36, "bold")
            )

    def draw_block(self, x, y, color):
        x0 = self.offset_x + x * self.cell_size
        y0 = self.offset_y + y * self.cell_size
        self.canvas.create_rectangle(
            x0, y0,
            x0 + self.cell_size,
            y0 + self.cell_size,
            fill=color,
            outline="black"
        )

    def handle_key(self, event):
        if event.keysym.lower() == 'q':
            self.root.destroy()
            return

        if not self.running:
            return

        if event.keysym.lower() == 'p':
            self.toggle_pause()
            return

        if self.paused:
            return

        key = event.keysym
        if key == "Left":
            self.move_piece(-1, 0)
        elif key == "Right":
            self.move_piece(1, 0)
        elif key == "Down":
            self.move_piece(0, 1)
        elif key == "Up":
            self.rotate_piece()

        self.draw()

    def toggle_pause(self):
        if self.paused:
            self.paused = False
            self.pause_time += time.time() - self.pause_start
            self.game_loop()
        else:
            self.paused = True
            self.pause_start = time.time()
        self.draw()

if __name__ == "__main__":
    root = tk.Tk()
    game = InfiniteTetris(root)
    root.mainloop()

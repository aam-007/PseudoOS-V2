import tkinter as tk
import random
import time
import os
import sys

class SnakeGame:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Snake Game")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.user_dir = os.path.join("users", self.username, "snake_game")
        os.makedirs(self.user_dir, exist_ok=True)
        self.high_score_file = os.path.join(self.user_dir, "high_score.txt")

        self.cell_size = 20
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.cols = self.width // self.cell_size
        self.rows = (self.height - 60) // self.cell_size

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.score = 0
        self.high_score = 0
        self.start_time = None
        self.direction = 'Right'
        self.running = False
        self.snake = []
        self.food = None
        self.paused = False
        self.pause_time = 0

        self.load_high_score()
        self.show_splash_screen()

    def show_splash_screen(self):
        self.canvas.delete("all")

        self.canvas.create_text(
            self.width // 2,
            self.height // 2 - 60,
            text="S N A K E   G A M E",
            font=("Courier New", 48, "bold"),
            fill="#00FF00"
        )

        self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text="Press any key to start",
            font=("Courier New", 20),
            fill="#00FF00"
        )

        self.canvas.create_text(
            self.width // 2,
            self.height // 2 + 40,
            text="Arrow keys to move | P to pause | ESC to exit",
            font=("Courier New", 14),
            fill="#00FF00"
        )

        self.root.bind("<Key>", self.start_game)

    def start_game(self, event=None):
        self.root.unbind("<Key>")
        self.root.bind("<KeyPress>", self.handle_key)
        self.canvas.delete("all")
        self.start_time = time.time()
        self.running = True
        self.paused = False
        self.pause_time = 0
        self.score = 0
        self.direction = 'Right'
        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.spawn_food()
        self.game_loop()

    def game_loop(self):
        if not self.running or self.paused:
            return

        self.move_snake()

        if self.check_collisions():
            self.running = False
            self.save_high_score()
            self.canvas.create_text(self.width // 2, self.height // 2,
                                    text="GAME OVER", font=("Courier New", 36), fill="red")
            self.canvas.create_text(self.width // 2, self.height // 2 + 50,
                                    text="Press any key to restart", font=("Courier New", 18), fill="white")
            self.root.bind("<Key>", self.start_game)
            return

        self.draw()
        self.root.after(100, self.game_loop)

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = {
            'Up': (0, -1),
            'Down': (0, 1),
            'Left': (-1, 0),
            'Right': (1, 0)
        }[self.direction]

        new_head = (head_x + dx, head_y + dy)
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            self.snake.pop()

    def check_collisions(self):
        head = self.snake[0]
        return (
            head in self.snake[1:] or
            head[0] < 0 or head[1] < 0 or head[0] >= self.cols or head[1] >= self.rows
        )

    def spawn_food(self):
        while True:
            x = random.randint(0, self.cols - 1)
            y = random.randint(0, self.rows - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                return

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.snake:
            self.canvas.create_rectangle(
                x * self.cell_size,
                y * self.cell_size,
                (x + 1) * self.cell_size,
                (y + 1) * self.cell_size,
                fill="#00FF00"
            )

        fx, fy = self.food
        self.canvas.create_oval(
            fx * self.cell_size,
            fy * self.cell_size,
            (fx + 1) * self.cell_size,
            (fy + 1) * self.cell_size,
            fill="red"
        )

        elapsed = int(time.time() - self.start_time - self.pause_time)
        mins = elapsed // 60
        secs = elapsed % 60
        current_time = time.strftime("%A, %d %B %Y | %H:%M:%S")

        info = (
            f"Score: {self.score}    |    "
            f"Time Alive: {mins}m {secs}s    |    "
            f"🏆 High Score: {self.high_score}    |    "
            f"{current_time}"
        )

        self.canvas.create_text(
            self.width // 2,
            self.height - 30,
            text=info,
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

    def handle_key(self, event):
        key = event.keysym
        if key in ['Up', 'Down', 'Left', 'Right']:
            opposites = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
            if key != opposites.get(self.direction):
                self.direction = key
        elif key.lower() == 'p':
            self.toggle_pause()
        elif key == 'Escape':
            self.root.destroy()

    def toggle_pause(self):
        if not self.running:
            return
        self.paused = not self.paused
        if self.paused:
            self.pause_start = time.time()
            self.draw()
        else:
            self.pause_time += time.time() - self.pause_start
            self.game_loop()

    def load_high_score(self):
        if os.path.exists(self.high_score_file):
            with open(self.high_score_file, "r") as f:
                line = f.readline().strip()
                try:
                    self.high_score = int(line.split()[0])
                except Exception:
                    self.high_score = 0

    def save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            current_time = time.strftime("%A, %d %B %Y | %H:%M:%S")
            with open(self.high_score_file, "w") as f:
                f.write(f"{self.high_score} apples on {current_time}")

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = SnakeGame(root, username)
    root.mainloop()

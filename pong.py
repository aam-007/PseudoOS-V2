import tkinter as tk
import time
import random
import os
import sys
from datetime import datetime

class PongGame:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.user_dir = os.path.join("users", self.username, "pong")
        os.makedirs(self.user_dir, exist_ok=True)
        self.high_score_file = os.path.join(self.user_dir, "highscore.txt")

        self.root.title("Pong - PseudoOS")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()

        self.running = False
        self.paused = False
        self.difficulty = "Medium"
        self.difficulty_speeds = {"Easy": 5, "Medium": 7, "Hard": 10}
        self.ai_speed = {"Easy": 4, "Medium": 6, "Hard": 8}

        self.show_splash()

    def show_splash(self):
        self.canvas.delete("all")
        self.canvas.create_text(self.width//2, self.height//2 - 100, text="PONG", fill="#00FF00", font=("Courier New", 60, "bold"))
        self.canvas.create_text(self.width//2, self.height//2, text="Press Any Key to Continue", fill="#00FF00", font=("Courier New", 20))
        self.show_high_scores()
        self.root.bind("<Key>", self.show_menu)

    def show_high_scores(self):
        if os.path.exists(self.high_score_file):
            with open(self.high_score_file, "r") as f:
                lines = f.readlines()[-3:]  # show last 3 games
                if lines:
                    self.canvas.create_text(self.width//2, self.height//2 + 80, text="🏆 Recent Scores:", fill="#00FF00", font=("Courier New", 18, "bold"))
                    for i, line in enumerate(reversed(lines)):
                        self.canvas.create_text(self.width//2, self.height//2 + 110 + i*30, text=line.strip(), fill="#00FF00", font=("Courier New", 14))

    def show_menu(self, event=None):
        self.root.unbind("<Key>")
        self.canvas.delete("all")
        self.canvas.create_text(self.width//2, self.height//2 - 120, text="Select Difficulty", fill="#00FF00", font=("Courier New", 30, "bold"))
        self.canvas.create_text(self.width//2, self.height//2 - 40, text="1. Easy", fill="#00FF00", font=("Courier New", 24))
        self.canvas.create_text(self.width//2, self.height//2, text="2. Medium", fill="#00FF00", font=("Courier New", 24))
        self.canvas.create_text(self.width//2, self.height//2 + 40, text="3. Hard", fill="#00FF00", font=("Courier New", 24))
        self.root.bind("1", lambda e: self.start_game("Easy"))
        self.root.bind("2", lambda e: self.start_game("Medium"))
        self.root.bind("3", lambda e: self.start_game("Hard"))

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.root.unbind("1")
        self.root.unbind("2")
        self.root.unbind("3")

        self.canvas.delete("all")
        self.player_score = 0
        self.ai_score = 0
        self.running = True
        self.start_time = time.time()

        self.ball = self.canvas.create_oval(0, 0, 20, 20, fill="#00FF00")
        self.paddle = self.canvas.create_rectangle(0, 0, 20, 100, fill="#00FF00")
        self.ai_paddle = self.canvas.create_rectangle(0, 0, 20, 100, fill="#00FF00")

        self.ball_dx = random.choice([-1, 1]) * self.difficulty_speeds[difficulty]
        self.ball_dy = random.choice([-1, 1]) * self.difficulty_speeds[difficulty]

        self.canvas.moveto(self.ball, self.width // 2, self.height // 2)
        self.canvas.moveto(self.paddle, 30, self.height // 2 - 50)
        self.canvas.moveto(self.ai_paddle, self.width - 50, self.height // 2 - 50)

        self.score_text = self.canvas.create_text(self.width // 2, 30, fill="#00FF00", font=("Courier New", 20), text="")
        self.time_text = self.canvas.create_text(self.width // 2, 60, fill="#00FF00", font=("Courier New", 14), text="")

        self.root.bind("<Up>", self.move_up)
        self.root.bind("<Down>", self.move_down)
        self.root.bind("p", self.pause_game)
        self.root.bind("q", lambda e: self.root.destroy())

        self.update_game()

    def move_up(self, event):
        if not self.running or self.paused: return
        self.canvas.move(self.paddle, 0, -30)

    def move_down(self, event):
        if not self.running or self.paused: return
        self.canvas.move(self.paddle, 0, 30)

    def pause_game(self, event=None):
        self.paused = not self.paused
        if self.paused:
            self.canvas.create_text(self.width//2, self.height//2, text="⏸ PAUSED", fill="#FFFF00", font=("Courier New", 40), tag="pause")
        else:
            self.canvas.delete("pause")
            self.update_game()

    def update_game(self):
        if not self.running or self.paused:
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(self.paddle)
        ai_coords = self.canvas.coords(self.ai_paddle)

        if ball_coords[1] <= 0 or ball_coords[3] >= self.height:
            self.ball_dy *= -1

        if (ball_coords[0] <= paddle_coords[2] and
            paddle_coords[1] < ball_coords[3] and
            paddle_coords[3] > ball_coords[1]):
            self.ball_dx *= -1

        if (ball_coords[2] >= ai_coords[0] and
            ai_coords[1] < ball_coords[3] and
            ai_coords[3] > ball_coords[1]):
            self.ball_dx *= -1

        if ball_coords[0] <= 0:
            self.ai_score += 1
            self.reset_ball()
        elif ball_coords[2] >= self.width:
            self.player_score += 1
            self.reset_ball()

        ball_y_center = (ball_coords[1] + ball_coords[3]) / 2
        ai_center = (ai_coords[1] + ai_coords[3]) / 2
        if ball_y_center < ai_center:
            self.canvas.move(self.ai_paddle, 0, -self.ai_speed[self.difficulty])
        elif ball_y_center > ai_center:
            self.canvas.move(self.ai_paddle, 0, self.ai_speed[self.difficulty])

        elapsed = int(time.time() - self.start_time)
        current_time = datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")

        self.canvas.itemconfig(self.score_text, text=f"YOU: {self.player_score}   AI: {self.ai_score}")
        self.canvas.itemconfig(self.time_text, text=f"Time Elapsed: {elapsed}s | {current_time}")

        self.root.after(20, self.update_game)

    def reset_ball(self):
        self.canvas.moveto(self.ball, self.width // 2, self.height // 2)
        self.ball_dx *= -1
        self.ball_dy = random.choice([-1, 1]) * self.difficulty_speeds[self.difficulty]

        if self.player_score >= 10 or self.ai_score >= 10:
            self.running = False
            self.save_high_score()
            self.show_game_over()

    def show_game_over(self):
        self.canvas.create_text(self.width//2, self.height//2 - 50, text="Game Over", fill="#00FF00", font=("Courier New", 40))
        self.canvas.create_text(self.width//2, self.height//2, text=f"Final Score - YOU: {self.player_score} | AI: {self.ai_score}", fill="#00FF00", font=("Courier New", 20))
        self.canvas.create_text(self.width//2, self.height//2 + 40, text="Press Q to Quit", fill="#00FF00", font=("Courier New", 16))

    def save_high_score(self):
        timestamp = datetime.now().strftime("%A, %d %B %Y | %I:%M:%S %p")
        with open(self.high_score_file, "a") as f:
            f.write(f"🏆 {self.player_score} vs {self.ai_score} on {timestamp}\n")

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    root = tk.Tk()
    app = PongGame(root, username)
    root.mainloop()

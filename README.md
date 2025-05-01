# PseudoOS V2. 

A major improvement from V1, which was purely CLI based.

PseudoOS – A Retro Desktop Operating System Simulator

# 🖥️ PseudoOS v2 – A Retro Desktop Operating System Simulator

**PseudoOS** is a full-screen Python-based retro desktop simulation built using `tkinter`. It mimics a vintage operating system and comes packed with classic-style utilities and mini-games. Designed for fun, learning, and nostalgia, PseudoOS combines the look and feel of an old-school GUI with modern Python scripting.

Showcase: (https://youtu.be/Xwd8XWuO6MI?si=1Fpd5lNQXF2kd3zI) 

---

## 🧰 Included Applications

### 🗂️ System Utilities
- **My Computer** – Explore a simulated file system per user
- **Terminal** – Execute simple commands in a Python-based shell
- **Notes** – Create and save plain text notes
- **Calculator** – Basic arithmetic calculator

### 🎮 Games
- **Snake** – Classic grid-based snake game
- **Pong** – 2-player paddle game
- **Tetris** – Block puzzle game
- **Pathfinder** – Visualizes pathfinding algorithms (like A*)
- **Maze** – 3D retro-style raycasting maze exploration game

---

## 🖼️ UI Features

- 🖥️ **Fullscreen Interface** – Immersive OS-like experience  
- 🧑 **User Profiles** – Separate user data and directories  
- 🧱 **Desktop Icons** – Launch apps with a click  
- 🕒 **Taskbar** – Real-time date & clock, shutdown option  
- ❌ **Graceful Exit** – Exit to desktop or shutdown the OS simulation

---

## 📂 File Structure

```bash
pseudo-os/
├── desktop.py          # Main PseudoOS environment
├── calculator.py       # Calculator app
├── terminal.py         # Shell-like terminal
├── notes.py            # Text editor
├── my_computer.py      # File browser
├── snake.py            # Snake game
├── pong.py             # Pong game
├── tetris.py           # Tetris game
├── pathfinder.py       # Pathfinding visualizer
├── maze.py             # 3D raycasting maze game
├── shutdown.py         # Shutdown/exit handler
├── users/              # User directories
└── README.md

⚙️ Requirements

    Python 3.x

    No external libraries required
    (Everything is built using tkinter, os, sys, math, and datetime)




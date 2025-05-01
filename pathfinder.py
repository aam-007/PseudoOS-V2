import tkinter as tk
from tkinter import messagebox
import datetime
import sys
import subprocess
import heapq
from collections import deque

# --- Pathfinding Algorithms ---
def bfs(grid, start, end, cols, rows):
    queue = deque([start])
    visited = {start: None}
    
    while queue:
        current = queue.popleft()
        if current == end:
            break
            
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x, y = current[0]+dx, current[1]+dy
            if (0 <= x < cols and 0 <= y < rows and
                grid[y][x] != 1 and (x,y) not in visited):
                visited[(x,y)] = current
                queue.append((x,y))
                
    return reconstruct_path(visited, end)

def dfs(grid, start, end, cols, rows):
    stack = [start]
    visited = {start: None}
    
    while stack:
        current = stack.pop()
        if current == end:
            break
            
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x, y = current[0]+dx, current[1]+dy
            if (0 <= x < cols and 0 <= y < rows and
                grid[y][x] != 1 and (x,y) not in visited):
                visited[(x,y)] = current
                stack.append((x,y))
                
    return reconstruct_path(visited, end)

def dijkstra(grid, start, end, cols, rows):
    heap = [(0, start)]
    visited = {start: None}
    cost = {start: 0}
    
    while heap:
        current_cost, current = heapq.heappop(heap)
        if current == end:
            break
            
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x, y = current[0]+dx, current[1]+dy
            new_cost = current_cost + 1
            if (0 <= x < cols and 0 <= y < rows and
                grid[y][x] != 1 and 
                new_cost < cost.get((x,y), float('inf'))):
                cost[(x,y)] = new_cost
                visited[(x,y)] = current
                heapq.heappush(heap, (new_cost, (x,y)))
                
    return reconstruct_path(visited, end)

def greedy_bfs(grid, start, end, cols, rows):
    def heuristic(pos):
        return abs(pos[0]-end[0]) + abs(pos[1]-end[1])
        
    heap = [(heuristic(start), start)]
    visited = {start: None}
    
    while heap:
        _, current = heapq.heappop(heap)
        if current == end:
            break
            
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x, y = current[0]+dx, current[1]+dy
            if (0 <= x < cols and 0 <= y < rows and
                grid[y][x] != 1 and (x,y) not in visited):
                visited[(x,y)] = current
                heapq.heappush(heap, (heuristic((x,y)), (x,y)))
                
    return reconstruct_path(visited, end)

def astar(grid, start, end, cols, rows):
    def heuristic(pos):
        return abs(pos[0]-end[0]) + abs(pos[1]-end[1])
        
    heap = [(heuristic(start), 0, start)]
    visited = {start: None}
    cost = {start: 0}
    
    while heap:
        _, current_cost, current = heapq.heappop(heap)
        if current == end:
            break
            
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x, y = current[0]+dx, current[1]+dy
            new_cost = current_cost + 1
            if (0 <= x < cols and 0 <= y < rows and
                grid[y][x] != 1 and 
                new_cost < cost.get((x,y), float('inf'))):
                cost[(x,y)] = new_cost
                visited[(x,y)] = current
                heapq.heappush(heap, (new_cost + heuristic((x,y)), new_cost, (x,y)))
                
    return reconstruct_path(visited, end)

def reconstruct_path(visited, end):
    if end not in visited:
        return []
        
    path = []
    current = end
    while current:
        path.append(current)
        current = visited.get(current)
        
    return path[::-1]

# --- GUI Application ---
class PathfinderOS(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Pathfinder OS")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")
        self.option_add("*Font", ("Courier New", 14))
        
        self.algorithms = {
            "A* Search": astar,
            "Dijkstra": dijkstra,
            "Breadth-First Search": bfs,
            "Depth-First Search": dfs,
            "Greedy Best-First Search": greedy_bfs
        }
        
        self.show_main_menu()

    def show_main_menu(self):
        if hasattr(self, "grid_frame"):
            self.grid_frame.destroy()
            
        self.menu_frame = MainMenu(self)
        self.menu_frame.pack(expand=True, fill=tk.BOTH)

    def show_grid(self, algorithm):
        self.menu_frame.destroy()
        self.grid_frame = GridFrame(self, self.username, algorithm)
        self.grid_frame.pack(expand=True, fill=tk.BOTH)

class MainMenu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(bg="black")
        self.create_widgets()

    def create_widgets(self):
        container = tk.Frame(self, bg="black")
        container.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(container, text="Select Algorithm:", 
                fg="#00FF00", bg="black").pack(pady=10)
        
        self.choice = tk.StringVar(value="A* Search")
        for name in self.parent.algorithms:
            tk.Radiobutton(container, text=name, variable=self.choice, value=name,
                          fg="#00FF00", bg="black", selectcolor="#111").pack(anchor="w", padx=20)
        
        tk.Button(container, text="Start", command=self.start_grid,
                 fg="#00FF00", bg="black").pack(pady=20)
        tk.Button(container, text="Exit", command=self.parent.destroy,
                 fg="#00FF00", bg="black").pack(pady=10)

    def start_grid(self):
        algorithm = self.parent.algorithms[self.choice.get()]
        self.parent.show_grid(algorithm)

class GridFrame(tk.Frame):
    def __init__(self, parent, username, algorithm):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.algorithm = algorithm
        self.configure(bg="black")
        self.setup_vars()
        self.create_widgets()
        self.setup_bindings()

    def setup_vars(self):
        self.start = None
        self.end = None
        self.cols, self.rows = 30, 20
        self.grid = [[0]*self.cols for _ in range(self.rows)]
        self.dragging = False
        self.erase_mode = False
        self.cell_size = min(
            self.winfo_screenwidth() // self.cols,
            (self.winfo_screenheight() - 100) // self.rows
        )

    def create_widgets(self):
        # Top Bar
        top = tk.Frame(self, bg="black")
        top.pack(fill=tk.X)
        
        self.clock = tk.Label(top, fg="#00FF00", bg="black")
        self.clock.pack(side=tk.LEFT, padx=20)
        
        tk.Button(top, text="Main Menu", command=self.parent.show_main_menu,
                 fg="#00FF00", bg="black").pack(side=tk.RIGHT, padx=20)
        
        # Grid Canvas
        self.canvas = tk.Canvas(self, bg="black",
                              width=self.cols*self.cell_size,
                              height=self.rows*self.cell_size)
        self.canvas.pack(pady=10)
        self.draw_grid()
        
        # Controls
        ctrl = tk.Frame(self, bg="black")
        ctrl.pack(fill=tk.X)
        
        tk.Button(ctrl, text="Find Path", command=self.find_path,
                 fg="#00FF00", bg="black").pack(side=tk.LEFT, padx=20)
        tk.Button(ctrl, text="Clear All", command=self.clear_all,
                 fg="#00FF00", bg="black").pack(side=tk.LEFT, padx=20)
        tk.Button(ctrl, text="Clear Path", command=self.clear_path,
                 fg="#00FF00", bg="black").pack(side=tk.LEFT, padx=20)
        
        self.update_clock()

    def draw_grid(self):
        # Draw lines
        for i in range(self.cols+1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.rows*self.cell_size, fill="#222")
        for j in range(self.rows+1):
            y = j * self.cell_size
            self.canvas.create_line(0, y, self.cols*self.cell_size, y, fill="#222")

    def update_clock(self):
        time_str = datetime.datetime.now().strftime("%A, %d %B %Y  %H:%M:%S")
        self.clock.config(text=time_str)
        self.after(1000, self.update_clock)

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)
        self.canvas.bind("<ButtonRelease-1>", self.handle_release)
        self.bind("<Shift_L>", lambda _: setattr(self, 'erase_mode', True))
        self.bind("<KeyRelease-Shift_L>", lambda _: setattr(self, 'erase_mode', False))

    def handle_click(self, event):
        x, y = event.x//self.cell_size, event.y//self.cell_size
        if not (0 <= x < self.cols and 0 <= y < self.rows):
            return
            
        if not self.start:
            self.set_start(x, y)
        elif not self.end:
            self.set_end(x, y)
        else:
            self.dragging = True
            self.toggle_cell(x, y)

    def handle_drag(self, event):
        if not self.dragging:
            return
            
        x, y = event.x//self.cell_size, event.y//self.cell_size
        if (0 <= x < self.cols and 0 <= y < self.rows and
            (x, y) not in (self.start, self.end)):
            self.toggle_cell(x, y)

    def handle_release(self, event):
        self.dragging = False

    def toggle_cell(self, x, y):
        if self.erase_mode:
            if self.grid[y][x] == 1:
                self.grid[y][x] = 0
                self.draw_cell(x, y, "black")
        else:
            if self.grid[y][x] == 0:
                self.grid[y][x] = 1
                self.draw_cell(x, y, "green")

    def set_start(self, x, y):
        if self.start:
            self.draw_cell(*self.start, "black")
        self.start = (x, y)
        self.draw_cell(x, y, "blue")

    def set_end(self, x, y):
        if self.end:
            self.draw_cell(*self.end, "black")
        self.end = (x, y)
        self.draw_cell(x, y, "red")

    def draw_cell(self, x, y, color):
        x0 = x * self.cell_size
        y0 = y * self.cell_size
        self.canvas.create_rectangle(
            x0, y0, x0+self.cell_size, y0+self.cell_size,
            fill=color, outline=""
        )

    def clear_all(self):
        self.canvas.delete("all")
        self.setup_vars()
        self.draw_grid()
        self.update_clock()

    def clear_path(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.grid[y][x] == 0:
                    self.draw_cell(x, y, "black")
        if self.start:
            self.draw_cell(*self.start, "blue")
        if self.end:
            self.draw_cell(*self.end, "red")

    def find_path(self):
        if not self.start or not self.end:
            messagebox.showwarning("Pathfinder", "Set start and end points!")
            return
            
        path = self.algorithm(
            self.grid, self.start, self.end,
            self.cols, self.rows
        )
        
        if not path:
            messagebox.showinfo("Pathfinder", "No path found!")
            return
            
        self.animate_path(path)

    def animate_path(self, path):
        self.clear_path()
        
        for i, (x, y) in enumerate(path):
            if (x, y) in (self.start, self.end):
                continue
            self.after(50*i, lambda x=x, y=y: 
                self.draw_cell(x, y, "#FFFF00")
            )
        self.after(50*len(path), lambda: 
            messagebox.showinfo("Pathfinder", f"Path found! Length: {len(path)-1}")
        )

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "guest"
    app = PathfinderOS(username)
    app.mainloop()
import tkinter as tk
import random
import heapq

board = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

GOAL = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
window = tk.Tk()
window.title("8-Puzzle Game")
window.resizable(False, False)
window.configure(bg="#1a1a2e")

title = tk.Label(
    window,
    text="8-Puzzle Game",
    font=("Courier", 22, "bold"),
    bg="#1a1a2e",
    fg="#e94560"
)
title.pack(pady=(20, 10))

frame = tk.Frame(window, bg="#16213e", bd=4, relief="solid")
frame.pack(padx=30, pady=10)


def find_empty():
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                return r, c

def board_to_tuple(b):
    return tuple(b[r][c] for r in range(3) for c in range(3))

def tuple_to_board(t):
    return [[t[r * 3 + c] for c in range(3)] for r in range(3)]


def manhattan_distance(b):
    distance = 0
    for r in range(3):
        for c in range(3):
            value = b[r][c]
            if value != 0:
                goal_row = (value - 1) // 3
                goal_col = (value - 1) % 3
                distance += abs(r - goal_row) + abs(c - goal_col)
    return distance


def a_star(start):
    start_tuple = board_to_tuple(start)
    goal_tuple = board_to_tuple(GOAL)

    h = manhattan_distance(start)
    queue = [(h, 0, start_tuple, [])]
    visited = set()

    while queue:
        f, g, current_tuple, path = heapq.heappop(queue)

        if current_tuple in visited:
            continue
        visited.add(current_tuple)

        if current_tuple == goal_tuple:
            return path

        current_board = tuple_to_board(current_tuple)
        empty_r, empty_c = None, None
        for r in range(3):
            for c in range(3):
                if current_board[r][c] == 0:
                    empty_r, empty_c = r, c

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_r = empty_r + dr
            new_c = empty_c + dc

            if 0 <= new_r < 3 and 0 <= new_c < 3:
                new_board = [row[:] for row in current_board]
                new_board[empty_r][empty_c] = new_board[new_r][new_c]
                new_board[new_r][new_c] = 0

                new_tuple = board_to_tuple(new_board)
                if new_tuple not in visited:
                    new_g = g + 1
                    new_h = manhattan_distance(new_board)
                    new_f = new_g + new_h
                    new_path = path + [(new_r, new_c)]
                    heapq.heappush(queue, (new_f, new_g, new_tuple, new_path))

    return []


def animate_solution(steps, index=0):
    if index >= len(steps):
        win_label.config(text="🎉 Solved by AI!", fg="#00ff88")
        return

    move_r, move_c = steps[index]
    empty_row, empty_col = find_empty()

    board[empty_row][empty_col] = board[move_r][move_c]
    board[move_r][move_c] = 0
    draw_board()

    window.after(400, animate_solution, steps, index + 1)


def solve_board(event=None):
    win_label.config(text="🤔 Thinking...", fg="#f5a623")
    window.update()

    solution = a_star(board)

    if solution:
        win_label.config(text="")
        animate_solution(solution)
    else:
        win_label.config(text="❌ No solution found!", fg="#e94560")

def shuffle_board(event=None):
    win_label.config(text="")
    for _ in range(200):
        empty_row, empty_col = find_empty()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        random.shuffle(directions)
        for dr, dc in directions:
            new_row = empty_row + dr
            new_col = empty_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                board[empty_row][empty_col] = board[new_row][new_col]
                board[new_row][new_col] = 0
                break
    draw_board()


def move_tile(row, col):
    empty_row, empty_col = find_empty()
    row_diff = abs(row - empty_row)
    col_diff = abs(col - empty_col)
    is_neighbor = (row_diff == 1 and col_diff == 0) or (row_diff == 0 and col_diff == 1)
    if is_neighbor:
        board[empty_row][empty_col] = board[row][col]
        board[row][col] = 0
        draw_board()
        check_win()


def check_win():
    if board == GOAL:
        win_label.config(text="🎉 You solved it!", fg="#00ff88")


def draw_board():
    for widget in frame.winfo_children():
        widget.destroy()

    for row in range(3):
        for col in range(3):
            number = board[row][col]
            if number == 0:
                
                cell = tk.Label(
                    frame,
                    text="",
                    width=4,
                    height=2,
                    font=("Courier", 30, "bold"),
                    bg="#0f3460",
                    relief="flat"
                )
                cell.grid(row=row, column=col, padx=5, pady=5)
            else:
               
                cell = tk.Label(
                    frame,
                    text=str(number),
                    width=4,
                    height=2,
                    font=("Courier", 30, "bold"),
                    bg="#16213e",
                    fg="#e94560",
                    relief="raised",
                    bd=3,
                    cursor="hand2",
                )
                cell.grid(row=row, column=col, padx=5, pady=5)
                
                cell.bind("<Button-1>", lambda e, r=row, c=col: move_tile(r, c))


buttons_frame = tk.Frame(window, bg="#1a1a2e")
buttons_frame.pack(pady=10)

shuffle_btn = tk.Label(
    buttons_frame,
    text="🔀 Shuffle",
    font=("Courier", 14, "bold"),
    bg="#7b2d8b",
    fg="white",
    relief="raised",
    bd=3,
    padx=20,
    pady=8,
    cursor="hand2",
)
shuffle_btn.pack(side="left", padx=10)
shuffle_btn.bind("<Button-1>", shuffle_board)

solve_btn = tk.Label(
    buttons_frame,
    text="🤖 Solve (A*)",
    font=("Courier", 14, "bold"),
    bg="#00916e",
    fg="white",
    relief="raised",
    bd=3,
    padx=20,
    pady=8,
    cursor="hand2",
)
solve_btn.pack(side="left", padx=10)
solve_btn.bind("<Button-1>", solve_board)

win_label = tk.Label(
    window,
    text="",
    font=("Courier", 16, "bold"),
    bg="#1a1a2e",
    fg="#00ff88"
)
win_label.pack(pady=10)

draw_board()


window.mainloop()
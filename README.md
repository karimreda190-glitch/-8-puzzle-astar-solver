# 8-Puzzle Solver

A Python implementation of the classic 8-puzzle game with an AI solver built on the A* search algorithm.

## Overview

The game runs on a 3x3 grid. You move tiles into the empty space until they reach order from 1 to 8. Play manually, or press Solve and watch the AI find the shortest path automatically.

## Features

- Manual tile movement with mouse clicks
- Guaranteed solvable shuffle (200 random valid moves from the goal state)
- AI solver using A* search with Manhattan Distance heuristic
- Step by step animation of the solution

## Technologies

- Python 3
- Tkinter for the GUI
- A* search algorithm
- Manhattan Distance heuristic

## How A* Works

A* picks the next move using this formula:

f(n) = g(n) + h(n)

- g(n): steps already taken
- h(n): Manhattan Distance, an estimate of steps remaining
- f(n): total estimated cost

A* always expands the state with the lowest f(n) first. This makes it explore far fewer states than BFS, since the heuristic points the search toward the goal instead of checking every possible state blindly.

## Manhattan Distance

For each tile, the distance to its goal position is:

distance = abs(current_row - goal_row) + abs(current_col - goal_col)

The sum across all tiles gives the heuristic value for a board state.

## Installation

Clone the repo:
git clone https://github.com/karimreda190-glitch/-8-puzzle-astar-solver.git
cd 8puzzle-astar-solver

Make sure Tkinter is installed. On Mac:
python3 -m tkinter
brew install python-tk

Run 
python3 stage4_final.py

Controls

Click any tile next to the empty space to move it
Press Shuffle to scramble the board
Press Solve (A*) to let the AI solve it automatically

Project Structure
stage4_final.py   Main game file: GUI, A* solver, and game logic

Author
Karim Hashish, Delta University, Faculty of Artificial Intelligence

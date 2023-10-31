# maze_generator.py
import random

class MazeGenerator:
    def __init__(self, width, height,wall_size):
        self.width = width
        self.height = height
        self.wall_size = wall_size
        self.grid = [[1] * width for _ in range(height)]

    def generate_maze(self, start_x=0, start_y=0):
        stack = [(start_x, start_y)]

        while stack:
            current_x, current_y = stack[-1]
            self.grid[current_y][current_x] = 0

            neighbors = self.get_unvisited_neighbors(current_x, current_y)
            if neighbors:
                next_x, next_y = random.choice(neighbors)
                stack.append((next_x, next_y))
                self.grid[(current_y + next_y) // 2][(current_x + next_x) // 2] = 0
            else:
                stack.pop()

    def get_unvisited_neighbors(self, x, y):
        neighbors = []
        directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.width and 0 <= new_y < self.height and self.grid[new_y][new_x] == 1:
                neighbors.append((new_x, new_y))

        return neighbors

    def get_maze_layout(self):
        return self.grid

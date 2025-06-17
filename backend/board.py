import random
from logic import can_move


class Board:
    def __init__(self, size=4):
        self.size = size
        self.grid = [[0]*size for _ in range(size)]
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empties = [(r,c) for r in range(self.size)
                          for c in range(self.size)
                          if self.grid[r][c]==0]
        if not empties: return
        r,c = random.choice(empties)
        self.grid[r][c] = 4 if random.random()<0.1 else 2

    def can_move(self):
        return can_move(self.grid)

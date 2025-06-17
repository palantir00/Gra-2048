import uuid
from board import Board
from logic import move

class GameSession:
    def __init__(self, size=4):
        self.id = str(uuid.uuid4())
        self.board = Board(size)
        self.score = 0

    def move(self, direction):
        new_grid, gained, moved = move(self.board.grid, direction)
        if moved:
            self.board.grid = new_grid
            self.score += gained
            self.board.spawn_tile()
        over = not self.board.can_move()
        return moved, gained, over

    def hint(self):
        # prosta heurystyka: dla każdego z 4 ruchów policz
        # ile pustych pól po ruchu zostanie i wybierz max
        best = None; max_empty=-1
        for d in ['up','down','left','right']:
            g2,_,m = move([row[:] for row in self.board.grid], d)
            if not m: continue
            empty = sum(r.count(0) for r in g2)
            if empty>max_empty:
                max_empty, best = empty, d
        return best
    def to_dict(self):
        return {'game_id': self.id, 'board': self.board.grid, 'score': self.score}

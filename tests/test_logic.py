import pytest
from logic import compress, merge, move, can_move

def test_compress_and_merge():
    row=[2,0,2,4]
    assert compress(row)==[2,2,4,0]
    merged, gained = merge([2,2,4,0])
    assert merged == [4,4,0,0]
    assert gained == 4

def test_can_move_false():
    full = [[2,4,8,16]]*4
    assert not can_move(full)

def test_move_left(monkeypatch):
    from board import Board
    b = Board(4)
    b.grid = [[2,2,0,0]] + [[0]*4]*3
    def fake_spawn(self): self.grid[0][2]=2
    monkeypatch.setattr(Board, 'spawn_tile', fake_spawn)
    new, gained, moved = move(b.grid, 'left')
    assert moved
    assert gained==4

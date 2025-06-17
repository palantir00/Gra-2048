import pytest
from backend.logic import compress, merge, move, can_move
from backend.board import Board

def test_compress_and_merge():
    row = [2,0,2,4]
    assert compress(row) == [2,2,4,0]
    merged, gained = merge([2,2,4,0])
    assert merged == [4,4,0,0]
    assert gained == 4

def test_can_move_false():
    full = [
        [2,  4,  8, 16],
        [16, 8,  4,  2 ],
        [2,  4,  8, 16],
        [16, 8,  4,  2 ],
    ]
    assert not can_move(full)


def test_move_left(monkeypatch):
    b = Board(4)
    b.grid = [[2,2,0,0]] + [[0]*4 for _ in range(3)]

    def fake_spawn(self):
        self.grid[0][1] = 2
    monkeypatch.setattr(Board, 'spawn_tile', fake_spawn)

    new_board, gained, moved = move(b, 'left')

    assert moved is True
    assert gained == 4

    expected = [[4,2,0,0]] + [[0]*4 for _ in range(3)]
    assert new_board.grid == expected

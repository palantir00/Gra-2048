import pytest
from backend.logic import compress, merge, move, can_move

def test_compress_and_merge():
    row = [2, 0, 2, 4]
    assert compress(row) == [2, 2, 4, 0]
    merged, gained = merge([2, 2, 4, 0])
    assert merged == [4, 4, 0, 0]
    assert gained == 4

def test_can_move_false():
    full = [
        [2,  4,  8, 16],
        [16, 8,  4,  2],
        [2,  4,  8, 16],
        [16, 8,  4,  2],
    ]
    assert not can_move(full)

def test_move_left():
    # przygotowujemy samą macierz (grid), bez żadnych Board czy spawn_tile
    grid = [[2, 2, 0, 0]] + [[0]*4 for _ in range(3)]
    new_grid, gained, moved = move(grid, 'left')

    assert moved is True     # udało się wykonać ruch
    assert gained == 4       # 2+2 -> 4 punkty

    # po merge [2,2,0,0] → [4,0,0,0]
    expected = [[4, 0, 0, 0]] + [[0]*4 for _ in range(3)]
    assert new_grid == expected

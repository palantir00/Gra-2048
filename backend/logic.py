# backend/logic.py

def compress(row):
    """Przesuwa wszystkie niezerowe wartości w lewo."""
    new = [x for x in row if x != 0]
    return new + [0] * (len(row) - len(new))

def merge(row):
    """
    Łączy pary identycznych kafelków idących w lewo:
    [2,2,4,0] → [4,4,0,0], zyskując score = 4.
    """
    row = compress(row)
    score = 0
    for i in range(len(row) - 1):
        if row[i] != 0 and row[i] == row[i + 1]:
            row[i] *= 2
            score += row[i]
            row[i + 1] = 0
    return compress(row), score

def move(grid, direction):
    """
    Wykonuje ruch w jednym z 4 kierunków.
    Zwraca: (nowy_grid, gained_score, moved_flag).
    """
    N = len(grid)
    moved = False
    total_score = 0
    # skopiuj całą siatkę, będziemy do niej zapisywać
    new_grid = [row[:] for row in grid]

    if direction in ("left", "right"):
        for i in range(N):
            row = grid[i][:]
            original = row[:]
            # jeśli right, odwróć, potem merge, potem odwróć z powrotem
            if direction == "right":
                row = row[::-1]

            merged, score = merge(row)

            if direction == "right":
                merged = merged[::-1]

            new_grid[i] = merged
            total_score += score
            if merged != original:
                moved = True

    elif direction in ("up", "down"):
        for j in range(N):
            # wyciągnij kolumnę
            col = [grid[i][j] for i in range(N)]
            original = col[:]

            if direction == "down":
                col = col[::-1]

            merged, score = merge(col)

            if direction == "down":
                merged = merged[::-1]

            # wpisz z powrotem do new_grid
            for i in range(N):
                new_grid[i][j] = merged[i]

            total_score += score
            if merged != original:
                moved = True

    else:
        # nieznany kierunek
        return grid, 0, False

    return new_grid, total_score, moved

def can_move(grid):
    """
    Sprawdza, czy da się wykonać jeszcze jakiś ruch:
    - jest puste pole, albo
    - obok siebie są dwa jednakowe kafelki.
    """
    N = len(grid)
    for r in range(N):
        for c in range(N):
            if grid[r][c] == 0:
                return True
            for dr, dc in ((1, 0), (0, 1)):
                nr, nc = r + dr, c + dc
                if nr < N and nc < N and grid[nr][nc] == grid[r][c]:
                    return True
    return False

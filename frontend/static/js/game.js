let gameId, board, score, best = 0;
const gridEl = document.getElementById('grid');
const scoreEl = document.getElementById('score');
const bestEl  = document.getElementById('best');
const hintBtn = document.getElementById('hintBtn');
const restartBtn = document.getElementById('restart');

async function start() {
  const res = await fetch('/games', { method: 'POST' });
  const data = await res.json();
  gameId = data.game_id;
  board  = data.board;
  score  = data.score;
  render();
}

function render() {
  // aktualizuj wynik
  scoreEl.textContent = score;
  best = Math.max(best, score);
  bestEl.textContent  = best;

  // odśwież grid
  gridEl.innerHTML = '';
  board.flat().forEach(value => {
    const cell = document.createElement('div');
    cell.className = 'grid-cell' + (value ? ` tile-${value}` : '');
    const inner = document.createElement('div');
    inner.className = 'inner';
    if (value) inner.textContent = value;
    cell.appendChild(inner);
    gridEl.appendChild(cell);
  });
}

async function doMove(dir) {
  const res = await fetch(`/games/${gameId}/move`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ direction: dir })
  });
  const data = await res.json();
  if (data.moved) {
    board = data.board;
    score = data.score;
    render();
    if (data.gameOver) alert('Koniec gry!');
  }
}

document.addEventListener('keydown', e => {
  const map = {
    ArrowUp:    'up',
    ArrowDown:  'down',
    ArrowLeft:  'left',
    ArrowRight: 'right'
  };
  if (map[e.key]) {
    e.preventDefault();
    doMove(map[e.key]);
  }
});

hintBtn.addEventListener('click', async () => {
  const res = await fetch(`/games/${gameId}/hint`);
  const { hint } = await res.json();
  alert('Sugerowany ruch: ' + hint);
});

restartBtn.addEventListener('click', start);

// ruszamy po załadowaniu
window.addEventListener('load', start);

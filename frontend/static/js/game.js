let gameId, board, score, best = 0;
let username = null;

const startScreen     = document.getElementById('startScreen');
const usernameInput   = document.getElementById('usernameInput');
const startBtn        = document.getElementById('startBtn');

const gameWrapper     = document.getElementById('gameWrapper');
const gridEl          = document.getElementById('grid');
const scoreEl         = document.getElementById('score');
const bestEl          = document.getElementById('best');
const hintBtn         = document.getElementById('hintBtn');
const restartBtn      = document.getElementById('restart');

const scoreboard      = document.getElementById('scoreboard');
const highscoresBody  = document.getElementById('highscoresBody');
const closeScoresBtn  = document.getElementById('closeScores');

let gameOverHandled = false;

startBtn.addEventListener('click', () => {
  const name = usernameInput.value.trim();
  if (!name) return alert('Proszę podać swoją nazwę!');
  username = name;
  startScreen.classList.add('hidden');
  gameWrapper.classList.remove('hidden');
  initGame();
});

async function initGame() {
  gameOverHandled = false;
  scoreboard.classList.add('hidden');
  const res  = await fetch('/games', { method:'POST' });
  const data = await res.json();
  gameId = data.game_id;
  board  = data.board;
  score  = data.score;
  best   = 0;
  render();
}

function render() {
  scoreEl.textContent = score;
  best = Math.max(best, score);
  bestEl.textContent  = best;

  gridEl.innerHTML = '';
  board.flat().forEach(val => {
    const cell = document.createElement('div');
    cell.className = 'grid-cell' + (val ? ` tile-${val}` : '');
    const inner = document.createElement('div');
    inner.className = 'inner';
    if (val) inner.textContent = val;
    cell.appendChild(inner);
    gridEl.appendChild(cell);
  });
}

async function doMove(dir) {
  if (gameOverHandled) return;

  const res  = await fetch(`/games/${gameId}/move`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ direction: dir })
  });
  const data = await res.json();

  if (data.moved) {
    board = data.board;
    score = data.score;
    render();
  }

  if (data.gameOver && !gameOverHandled) {
    gameOverHandled = true;

    alert("Koniec gry");

    await fetch('/highscores', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: username, score })
    });

    await showHighscores();
  }
}

async function showHighscores() {
  console.log("▶️ showHighscores() called");
  const res  = await fetch('/highscores');
  const list = await res.json();
  console.log("▶️ dane z GET /highscores:", list);

  highscoresBody.innerHTML = '';

  list.forEach((e, i) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${i+1}</td>
      <td>${e.name}</td>
      <td>${e.score}</td>
      <td>${new Date(e.date).toLocaleString()}</td>
    `;
    highscoresBody.appendChild(tr);
  });

  scoreboard.classList.remove('hidden');
  console.log("⚡ scoreboard powinien być widoczny");

  restartBtn.textContent = 'New Game';
  restartBtn.focus();
}


document.addEventListener('keydown', e => {
  const map = { ArrowUp:'up', ArrowDown:'down', ArrowLeft:'left', ArrowRight:'right' };
  if (map[e.key]) {
    e.preventDefault();
    doMove(map[e.key]);
  }
});

hintBtn.addEventListener('click', async () => {
  const res  = await fetch(`/games/${gameId}/hint`);
  const { hint } = await res.json();
  alert('Sugerowany ruch: ' + hint);
});
restartBtn.addEventListener('click', initGame);

closeScoresBtn.addEventListener('click', () => {
  scoreboard.classList.add('hidden');
});

// start
window.addEventListener('load', () => {
  startScreen.classList.remove('hidden');
});


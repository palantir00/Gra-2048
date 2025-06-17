# Gra-2048
# 2048 z AI-hint

## Opis
Klasyczna gra 2048 z opcją „Podpowiedz ruch” opartą na prostej heurystyce (maksymalizacja wolnych pól).

## Struktura projektu
- **backend/**: Flask API + SQLite  
- **frontend/**: HTML/CSS/JS + Canvas + AJAX  
- **tests/**: pytest  
- **.github/**: workflow CI  

## Instalacja
1. `cd backend && python3 -m venv venv && source venv/bin/activate`  
2. `pip install -r requirements.txt`  
3. Skonfiguruj `.env`  
4. `flask run`

## API
- `POST /games` – start nowej gry  
- `POST /games/<id>/move` – ruch `{direction: up|down|left|right}`  
- `GET /games/<id>/hint` – podpowiedź  
- `GET/POST /highscores` – ranking  

## Parametry w `.env`
- `DATABASE_URI` – URI SQLite  
- `MAX_TILE`, `HINT_EMPTY_WEIGHT`, `HINT_MERGE_WEIGHT`

## AI-hint
Testuje każdy z 4 ruchów, wybiera ten, który zostawia najwięcej pustych pól.


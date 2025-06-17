# Gra 2048 z podpowiedziami AI

Klasyczna gra 2048 w przeglądarce, rozszerzona o prostą funkcję „Podpowiedz ruch” korzystającą z heurystyki (maksymalizacja liczby wolnych pól).

---

## Spis treści

1. [Opis projektu](#opis-projektu)  
2. [Technologie](#technologie)  
3. [Struktura projektu](#struktura-projektu)  
4. [Instalacja](#instalacja)  
5. [Konfiguracja](#konfiguracja)  
6. [Uruchomienie](#uruchomienie)  
7. [API](#api)  
8. [Baza danych](#baza-danych)  
9. [Testy](#testy)  
10. [CI / CD](#ci--cd)  
11. [Przykład działania AI-podpowiedzi](#przykład-działania-ai-podpowiedzi)  
12. [Możliwości rozwoju](#możliwości-rozwoju)  

---

## Opis projektu

Ta aplikacja to webowa implementacja gry 2048:

- **Frontend**: HTML/CSS/JS z Canvasem do rysowania planszy, AJAX do komunikacji z backendem  
- **Backend**: Flask + REST API  
- **Baza danych**: MongoDB (ranking najlepszych wyników)  
- **Podpowiedź ruchu**: prosty algorytm heurystyczny zwracający kierunek ruchu  
- **Testy**: pytest do logiki gry  
- **CI/CD**: GitHub Actions uruchamiające lint i testy  

---

## Technologie

- Python 3.9+  
- Flask  
- Flask-PyMongo / pymongo  
- MongoDB Atlas  
- HTML5 / CSS3 / JavaScript (Canvas, Fetch/AJAX)  
- pytest  
- GitHub Actions  
- python-dotenv  

---

## Struktura projektu

```
Gra-2048/
├── backend/
│   ├── __init__.py
│   ├── app.py
│   ├── game.py
│   ├── board.py
│   ├── logic.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── css/
│       │   └── style.css
│       └── js/
│           └── game.js
├── tests/
│   └── test_logic.py
├── run.py
├── .env
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml
```

---

## Instalacja

1. **Sklonuj repozytorium**:  
   ```bash
   git clone https://github.com/<Twoje-Repo>/Gra-2048.git
   cd Gra-2048
   ```

2. **Utwórz i aktywuj virtualenv**:  
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Zainstaluj zależności**:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Konfiguracja

W pliku `.env` (w katalogu głównym) ustaw:

```dotenv
MONGODB_URI=<twoje_uri_do_MongoDB>
FLASK_ENV=development
MAX_TILE_LEVEL=2048
HEURISTIC_PARAMS=<opcjonalne parametry AI>
```

---

## Uruchomienie

### Metoda A: `run.py`

```bash
source venv/bin/activate
python run.py
```

### Metoda B: Flask-CLI

```bash
export FLASK_APP=backend.app
export FLASK_ENV=development
flask run
```

Serwer nasłuchuje domyślnie na `http://127.0.0.1:5000`.

---

## API

### `POST /games`

**Opis**: Tworzy nową grę  
**Response**:
```json
{
  "game_id": "uuid",
  "board": [[0,2,0,0]],
  "score": 0
}
```

### `POST /games/<game_id>/move`

**Opis**: Wykonuje ruch  
**Request**:
```json
{ "direction": "up, down, left, right" }
```

```

### `GET /games/<game_id>/hint`

**Opis**: Zwraca sugerowany ruch  
**Response**:
```json
{ "hint": "left" }
```

### `POST /highscores`

**Opis**: Zapisuje wynik do rankingu  
**Request**:
```json
{ "name": "Gracz", "score": 1234 }
```
**Response**: lista top 10 wpisów  
```json
[
  { "name": "Ala", "score": 2396, "date": "2025-06-17T14:29:15.523Z" }
]
```

### `GET /highscores`

**Opis**: Pobiera ranking top 10  
**Response**: jak wyżej

---

## Baza danych

- **MongoDB Atlas**  
- Kolekcja `highscores` ze schematem:
```json
{
  "name": "<string>",
  "score": "<int>",
  "date": "<ISODate>",
  "boardSize": "<int>"
}
```

---

## Testy

Uruchom testy logiki:
```bash
pytest tests/ -q
```

---

## CI / CD

Plik `.github/workflows/ci.yml` definiuje:

1. **checkout**  
2. **setup-python**  
3. `pip install -r requirements.txt`  
4. `flake8` + `mypy`  
5. `pytest --disable-warnings -q`  

---

## Przykład działania AI-podpowiedzi

1. `POST /games` → `{ "game_id": "...", ... }`  
2. `GET /games/<id>/hint` → `{ "hint": "right" }`  
3. Na froncie alert: “Sugerowany ruch: right”

---

## Możliwości rozwoju

- różne rozmiary planszy (5×5…15×15)  
- zaawansowana AI (minimax, MCTS)  
- PWA / offline support (IndexedDB)  
- dodatkowe tryby gry  

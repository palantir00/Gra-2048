# backend/app.py

import os
import uuid
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_pymongo import PyMongo
from dotenv import load_dotenv

# 1. Wczytanie .env
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URI")
if not MONGO_URI:
    raise RuntimeError("Brakuje MONGODB_URI w .env")

# 2. Ścieżka do frontend/
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")

# 3. Inicjalizacja Flask-a (serwujemy też pliki statyczne)
app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_DIR, "static"),
    static_url_path="/static"
)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

# 4. Import logic
from game import GameSession  # plik backend/game.py

# 5. Sesje gier w pamięci
games = {}

# 6. Prosty ping do weryfikacji
@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"pong": True})

# 7. Serwuj front-end
@app.route("/", methods=["GET"])
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

# 8. Pomocniczy GET /games (żeby GET /games nie zwracał 405)
@app.route("/games", methods=["GET"])
def games_help():
    return jsonify({"usage": "Send POST to /games to start a new game"})

# 9. POST /games – nowa gra
@app.route("/games", methods=["POST"])
def create_game():
    game = GameSession()
    games[game.id] = game
    return jsonify(game.to_dict())

# 10. POST /games/<id>/move
@app.route("/games/<game_id>/move", methods=["POST"])
def game_move(game_id):
    data = request.get_json() or {}
    direction = data.get("direction")
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404

    moved, gained, over = game.move(direction)

    # Zapis ruchu
    mongo.db.move_history.insert_one({
        "game_id": game_id,
        "direction": direction,
        "gained": gained,
        "timestamp": datetime.utcnow()
    })

    return jsonify({
        "board": game.board.grid,
        "score": game.score,
        "moved": moved,
        "gameOver": over
    })

# 11. GET /games/<id>/hint
@app.route("/games/<game_id>/hint", methods=["GET"])
def game_hint(game_id):
    game = games.get(game_id)
    if not game:
        return jsonify({"error": "Game not found"}), 404
    hint = game.hint()
    return jsonify({"hint": hint})

# 12. GET /highscores
@app.route("/highscores", methods=["GET"])
def get_highscores():
    docs = mongo.db.highscores.find().sort("score", -1).limit(10)
    result = []
    for d in docs:
        result.append({
            "name": d.get("name"),
            "score": d.get("score"),
            "date": d.get("date").isoformat()
        })
    return jsonify(result)

# 13. POST /highscores
@app.route("/highscores", methods=["POST"])
def post_highscore():
    data = request.get_json() or {}
    name = data.get("name")
    score = data.get("score")
    if not name or score is None:
        return jsonify({"error": "Missing name or score"}), 400
    mongo.db.highscores.insert_one({
        "name": name,
        "score": int(score),
        "date": datetime.utcnow()
    })
    return get_highscores()

# 14. Uruchomienie
if __name__ == "__main__":
    app.run(debug=True)

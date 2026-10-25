"""Flask REST API for the browser-based Hangman game."""

from __future__ import annotations

import secrets
from typing import Any

from flask import Flask, jsonify, request, send_from_directory

from game import GameOverError, HangmanGame
from word_manager import WordManager


def create_app(word_manager: WordManager | None = None) -> Flask:
    app = Flask(__name__, static_folder="static", static_url_path="/static")
    app.config["GAMES"] = {}
    app.config["WORD_MANAGER"] = word_manager or WordManager()

    def game_payload(game_id: str, game: HangmanGame) -> dict[str, Any]:
        return {"game_id": game_id, **game.to_dict()}

    def json_object() -> dict[str, Any] | None:
        if not request.is_json:
            return None
        body = request.get_json(silent=True)
        return body if isinstance(body, dict) else None

    @app.get("/")
    def index():
        return send_from_directory(app.static_folder, "index.html")

    @app.post("/api/games")
    def create_game():
        body = json_object()
        if body is None:
            return jsonify(error="Request body must be a JSON object"), 400
        if set(body) != {"difficulty"}:
            return jsonify(error="Request must contain only difficulty"), 400
        difficulty = body["difficulty"]
        try:
            game = HangmanGame.new_game(difficulty, word_manager=app.config["WORD_MANAGER"])
        except (ValueError, AttributeError) as exc:
            return jsonify(error=str(exc)), 400

        games: dict[str, HangmanGame] = app.config["GAMES"]
        game_id = secrets.token_urlsafe(16)
        while game_id in games:
            game_id = secrets.token_urlsafe(16)
        games[game_id] = game
        return jsonify(game_payload(game_id, game)), 201

    @app.get("/api/games/<game_id>")
    def get_game(game_id: str):
        game = app.config["GAMES"].get(game_id)
        if game is None:
            return jsonify(error="Game not found"), 404
        return jsonify(game_payload(game_id, game)), 200

    @app.post("/api/games/<game_id>/guess")
    def guess(game_id: str):
        game = app.config["GAMES"].get(game_id)
        if game is None:
            return jsonify(error="Game not found"), 404
        body = json_object()
        if body is None:
            return jsonify(error="Request body must be a JSON object"), 400
        if set(body) != {"letter"}:
            return jsonify(error="Request must contain only letter"), 400
        try:
            game.guess(body["letter"])
        except GameOverError as exc:
            return jsonify(error=str(exc)), 409
        except ValueError as exc:
            return jsonify(error=str(exc)), 400
        return jsonify(game_payload(game_id, game)), 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)

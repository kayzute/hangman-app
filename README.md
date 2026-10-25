# Hangman Game Engine

This project is a browser-based Hangman game. Its Python game engine remains
independent of Flask and the browser; Flask exposes the engine through a JSON
REST API, and the browser client communicates with that API.

## Use

```python
from game import HangmanGame

game = HangmanGame.new_game("easy")
print(game.to_dict())
game.guess("e")
print(game.to_dict())
```

`HangmanGame(word)` can also be used with a chosen word for deterministic
scenarios. `guess()` accepts one ASCII letter, case-insensitively, and returns
whether it was in the word. Invalid and duplicate guesses raise `ValueError`;
guesses after a win or loss raise `GameOverError`. State dictionaries omit the
answer while play is active and include it after the game ends.

Words are selected randomly from `words/easy.txt`, `words/medium.txt`, or
`words/hard.txt`. The default limit is six incorrect guesses.

## Verify

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Run the server

```bash
python server.py
```

The server listens at `http://127.0.0.1:5000`. The browser game is served at
`/`. Select a difficulty, start a new game, then use the on-screen alphabet or
your keyboard to guess. Start another game at any time with the new-game button.

## REST API

- `POST /api/games` with `{"difficulty":"medium"}` creates a game.
- `GET /api/games/{game_id}` returns its current state.
- `POST /api/games/{game_id}/guess` with `{"letter":"e"}` submits a guess.

Responses include the masked `pattern`, guessed and incorrect letters,
remaining guesses, and status. The answer is included only after the game ends.
Invalid requests return a JSON `error` and an appropriate 4xx status code.

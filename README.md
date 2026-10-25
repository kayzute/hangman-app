# Hangman Game Engine

This checkout implements the standalone Python game engine from the project
specification. The game and word manager have no Flask, browser, or terminal
interface dependencies.

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
python -m unittest discover -s tests -v
```

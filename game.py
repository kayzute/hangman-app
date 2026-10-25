"""UI-independent Hangman game engine."""

from __future__ import annotations

from word_manager import WordManager


class GameOverError(RuntimeError):
    """Raised when a guess is submitted after the game has ended."""


class HangmanGame:
    """Owns one Hangman game's secret word and state."""

    def __init__(self, word: str, max_incorrect_guesses: int = 6, difficulty: str | None = None):
        if not isinstance(word, str) or not word or not word.isascii() or not word.isalpha():
            raise ValueError("Word must contain only ASCII letters")
        if not isinstance(max_incorrect_guesses, int) or isinstance(max_incorrect_guesses, bool) or max_incorrect_guesses < 1:
            raise ValueError("Maximum incorrect guesses must be a positive integer")

        self._word = word.lower()
        self.max_incorrect_guesses = max_incorrect_guesses
        self.difficulty = difficulty.lower() if isinstance(difficulty, str) else difficulty
        self.guessed_letters: list[str] = []
        self.incorrect_letters: list[str] = []

    @classmethod
    def new_game(
        cls,
        difficulty: str = "medium",
        word_manager: WordManager | None = None,
        max_incorrect_guesses: int = 6,
    ) -> "HangmanGame":
        manager = word_manager or WordManager()
        word = manager.choose_word(difficulty)
        return cls(word, max_incorrect_guesses=max_incorrect_guesses, difficulty=difficulty.strip().lower())

    @property
    def pattern(self) -> str:
        return " ".join(letter if letter in self.guessed_letters else "_" for letter in self._word)

    @property
    def remaining_guesses(self) -> int:
        return self.max_incorrect_guesses - len(self.incorrect_letters)

    @property
    def status(self) -> str:
        if all(letter in self.guessed_letters for letter in set(self._word)):
            return "won"
        if self.remaining_guesses == 0:
            return "lost"
        return "playing"

    def guess(self, letter: str) -> bool:
        """Record a letter; return True if it occurs in the word.

        Invalid and repeated guesses raise ValueError. Guesses after a win or
        loss raise GameOverError and do not alter the game.
        """
        if self.status != "playing":
            raise GameOverError("The game has already ended")
        if not isinstance(letter, str) or len(letter) != 1 or not letter.isascii() or not letter.isalpha():
            raise ValueError("Guess must be a single letter from A to Z")
        letter = letter.lower()
        if letter in self.guessed_letters:
            raise ValueError(f"Letter {letter!r} has already been guessed")

        self.guessed_letters.append(letter)
        if letter not in self._word:
            self.incorrect_letters.append(letter)
            return False
        return True

    def to_dict(self) -> dict[str, object]:
        """Return client-safe state; reveal the answer only after the game ends."""
        state: dict[str, object] = {
            "pattern": self.pattern,
            "guessed_letters": list(self.guessed_letters),
            "incorrect_letters": list(self.incorrect_letters),
            "remaining_guesses": self.remaining_guesses,
            "status": self.status,
        }
        if self.difficulty is not None:
            state["difficulty"] = self.difficulty
        if self.status != "playing":
            state["word"] = self._word
        return state

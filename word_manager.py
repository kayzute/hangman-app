"""Load and select words for the Hangman game engine."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Protocol


DIFFICULTIES = ("easy", "medium", "hard")
DEFAULT_WORDS_DIR = Path(__file__).resolve().parent / "words"


class RandomSource(Protocol):
    def choice(self, sequence: list[str]) -> str: ...


class WordManager:
    """Loads validated word lists and chooses a random word by difficulty."""

    def __init__(self, words_dir: str | Path = DEFAULT_WORDS_DIR, rng: RandomSource | None = None):
        self.words_dir = Path(words_dir)
        self._rng = rng or random.Random()
        self._words: dict[str, list[str]] = {}

    def words_for(self, difficulty: str) -> list[str]:
        level = self._normalize_difficulty(difficulty)
        if level not in self._words:
            path = self.words_dir / f"{level}.txt"
            try:
                contents = path.read_text(encoding="utf-8")
            except OSError as exc:
                raise ValueError(f"Could not load the {level} word list: {path}") from exc

            words: list[str] = []
            seen: set[str] = set()
            for line in contents.splitlines():
                word = line.strip().lower()
                if word and word.isascii() and word.isalpha() and word not in seen:
                    words.append(word)
                    seen.add(word)
            if not words:
                raise ValueError(f"The {level} word list contains no valid words")
            self._words[level] = words
        return list(self._words[level])

    def choose_word(self, difficulty: str) -> str:
        return self._rng.choice(self.words_for(difficulty))

    @staticmethod
    def _normalize_difficulty(difficulty: str) -> str:
        if not isinstance(difficulty, str):
            raise ValueError("Difficulty must be easy, medium, or hard")
        level = difficulty.strip().lower()
        if level not in DIFFICULTIES:
            raise ValueError("Difficulty must be easy, medium, or hard")
        return level

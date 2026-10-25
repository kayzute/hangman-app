import unittest

from game import GameOverError, HangmanGame
from word_manager import WordManager


class FixedRandom:
    def __init__(self, selected=None):
        self.selected = selected

    def choice(self, values):
        return self.selected if self.selected in values else values[0]


class HangmanGameTests(unittest.TestCase):
    def test_initial_state_masks_every_letter(self):
        game = HangmanGame("apple")
        self.assertEqual(game.pattern, "_ _ _ _ _")
        self.assertEqual(game.remaining_guesses, 6)
        self.assertEqual(game.status, "playing")
        self.assertNotIn("word", game.to_dict())

    def test_correct_and_incorrect_guesses_update_state(self):
        game = HangmanGame("apple")
        self.assertTrue(game.guess("P"))
        self.assertEqual(game.pattern, "_ p p _ _")
        self.assertFalse(game.guess("z"))
        self.assertEqual(game.incorrect_letters, ["z"])
        self.assertEqual(game.remaining_guesses, 5)

    def test_invalid_and_duplicate_guesses_are_rejected_without_mutation(self):
        game = HangmanGame("apple")
        for guess in ("", "ab", "1", "é"):
            with self.subTest(guess=guess), self.assertRaises(ValueError):
                game.guess(guess)
        game.guess("a")
        with self.assertRaises(ValueError):
            game.guess("A")
        self.assertEqual(game.guessed_letters, ["a"])

    def test_win_reveals_word_and_blocks_more_guesses(self):
        game = HangmanGame("aba")
        game.guess("a")
        game.guess("b")
        self.assertEqual(game.status, "won")
        self.assertEqual(game.to_dict()["word"], "aba")
        with self.assertRaises(GameOverError):
            game.guess("c")

    def test_loss_reveals_word_and_blocks_more_guesses(self):
        game = HangmanGame("cat", max_incorrect_guesses=2)
        game.guess("x")
        game.guess("y")
        self.assertEqual(game.status, "lost")
        self.assertEqual(game.remaining_guesses, 0)
        self.assertEqual(game.to_dict()["word"], "cat")
        with self.assertRaises(GameOverError):
            game.guess("c")

    def test_game_can_select_word_by_difficulty(self):
        manager = WordManager(rng=FixedRandom("quizzically"))
        game = HangmanGame.new_game("hard", word_manager=manager)
        self.assertEqual(game.difficulty, "hard")
        self.assertEqual(game.pattern, "_ _ _ _ _ _ _ _ _ _ _")


class WordManagerTests(unittest.TestCase):
    def test_each_difficulty_selects_a_word(self):
        manager = WordManager(rng=FixedRandom())
        for difficulty in ("easy", "medium", "hard"):
            with self.subTest(difficulty=difficulty):
                word = manager.choose_word(difficulty)
                self.assertTrue(word.isascii() and word.isalpha())

    def test_invalid_difficulty_is_rejected(self):
        with self.assertRaises(ValueError):
            WordManager().choose_word("expert")


if __name__ == "__main__":
    unittest.main()

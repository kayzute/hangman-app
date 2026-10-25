import unittest

from server import create_app
from word_manager import WordManager


class FixedRandom:
    def choice(self, values):
        return "cat"


class HangmanApiTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(WordManager(rng=FixedRandom()))
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def start_game(self):
        response = self.client.post("/api/games", json={"difficulty": "easy"})
        self.assertEqual(response.status_code, 201)
        return response.get_json()

    def test_create_game_returns_client_safe_initial_state(self):
        state = self.start_game()
        self.assertTrue(state["game_id"])
        self.assertEqual(state["pattern"], "_ _ _")
        self.assertEqual(state["remaining_guesses"], 6)
        self.assertEqual(state["status"], "playing")
        self.assertNotIn("word", state)

    def test_get_game_returns_current_state_and_unknown_ids_404(self):
        state = self.start_game()
        response = self.client.get(f"/api/games/{state['game_id']}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["pattern"], "_ _ _")
        self.assertEqual(self.client.get("/api/games/missing").status_code, 404)

    def test_guess_updates_state_and_answer_is_only_revealed_after_win(self):
        state = self.start_game()
        game_id = state["game_id"]
        for letter in ("a", "c", "t"):
            response = self.client.post(f"/api/games/{game_id}/guess", json={"letter": letter})
            self.assertEqual(response.status_code, 200)
        finished = response.get_json()
        self.assertEqual(finished["status"], "won")
        self.assertEqual(finished["word"], "cat")
        self.assertEqual(self.client.post(f"/api/games/{game_id}/guess", json={"letter": "z"}).status_code, 409)

    def test_invalid_requests_and_missing_game_are_reported(self):
        self.assertEqual(self.client.post("/api/games", json={"difficulty": "expert"}).status_code, 400)
        self.assertEqual(self.client.post("/api/games", json={"difficulty": "easy", "word": "cat"}).status_code, 400)
        self.assertEqual(self.client.post("/api/games").status_code, 400)
        self.assertEqual(self.client.post("/api/games/missing/guess", json={"letter": "a"}).status_code, 404)

    def test_guess_input_is_validated_and_duplicates_rejected(self):
        game_id = self.start_game()["game_id"]
        self.assertEqual(self.client.post(f"/api/games/{game_id}/guess", json={"letter": "ab"}).status_code, 400)
        self.assertEqual(self.client.post(f"/api/games/{game_id}/guess", json={"letter": "a"}).status_code, 200)
        self.assertEqual(self.client.post(f"/api/games/{game_id}/guess", json={"letter": "a"}).status_code, 400)


if __name__ == "__main__":
    unittest.main()

# TODO — Web-Based Hangman Project

This roadmap adapts the broader project specification to the reduced assignment scope: a browser-based Hangman game with a Flask backend and an HTML/CSS/JavaScript frontend.

The game engine and word management remain independent of Flask and the browser. The server is authoritative and must not reveal the hidden word while a game is active.

## Implementation Rules

- Work through the phases in order and keep the application runnable after each phase.
- Preserve the separation between game logic, REST API, and browser presentation.
- Use JSON over HTTP for browser/server communication.
- Validate all client input on the server, even when the browser also validates it.
- Add automated checks while implementing features and complete the dedicated test/debug phase before deployment.
- Update the README when setup, behavior, API routes, or deployment instructions change.

## Phase 1 — Game Engine and Word Management

### Tasks

- [x] Set up the project structure for the Python engine and word lists.
- [x] Add Easy, Medium, and Hard word lists.
- [x] Load and validate word-list entries; remove duplicates.
- [x] Select a random word for a requested difficulty.
- [x] Reject unsupported difficulty values.
- [x] Implement a UI-independent `HangmanGame` class.
- [x] Track guessed and incorrect letters.
- [x] Validate one-letter guesses and reject invalid or duplicate guesses.
- [x] Display the masked word pattern and remaining incorrect guesses.
- [x] Detect wins and losses and prevent guesses after the game ends.
- [x] Reveal the answer only after the game ends.
- [x] Add unit tests for engine and word-management behavior.

### Completion Criteria

A game can be created and played entirely through Python without Flask or a browser. Core rules and difficulty-based word selection are covered by unit tests.

## Phase 2 — Flask Server and REST API

### Tasks

- [x] Add the Flask application and dependency configuration.
- [x] Serve the browser application from the Flask app.
- [x] Store active games in memory and assign each a unique game ID.
- [x] Implement `POST /api/games` to create a game for the requested difficulty.
- [x] Implement `GET /api/games/{game_id}` to return the current client-safe state.
- [x] Implement `POST /api/games/{game_id}/guess` to process a letter guess.
- [x] Return consistent JSON responses for successful requests and errors.
- [x] Use appropriate HTTP status codes for malformed requests, invalid input, and unknown game IDs.
- [x] Ensure active-game responses never include the hidden word.
- [x] Keep the server authoritative; do not accept a client-supplied answer or game outcome.
- [x] Document request and response shapes in the README.

### Completion Criteria

A complete game can be created and played using HTTP requests alone. The API returns enough state for a client to render the game without disclosing the answer during play.

## Phase 3 — Browser-Based Client

### Tasks

- [x] Create `static/index.html`, `static/style.css`, and `static/app.js`.
- [x] Provide Easy, Medium, and Hard difficulty selection.
- [x] Add a New Game/restart action.
- [x] Use `fetch()` to create games and submit guesses through the REST API.
- [x] Display the masked word, guessed letters, incorrect letters, and remaining guesses.
- [x] Provide an on-screen A–Z keyboard and disable letters already guessed or input after game end.
- [x] Draw and update the hangman graphic as incorrect guesses accumulate.
- [x] Show clear win/loss feedback and the answer after the game ends.
- [x] Show useful feedback when API requests fail.
- [x] Make the interface usable on desktop and mobile screen sizes.
- [x] Keep all game rules and the secret word on the server; browser code should only present API state and collect input.

### Completion Criteria

A player can start and finish a game in a browser. The interface reflects server state after each action and supports starting another game.

## Phase 4 — Testing and Debugging

### Tasks

- [ ] Run and maintain unit tests for the game engine and word management.
- [ ] Add API tests for game creation, state retrieval, guesses, validation errors, and unknown IDs.
- [ ] Test correct guesses, incorrect guesses, duplicate guesses, wins, losses, and attempts after game end.
- [ ] Test that the answer is absent from active-game API responses and available after completion.
- [ ] Test the browser-to-API flow for creating a game and submitting guesses.
- [ ] Exercise invalid input and server/network errors in the browser.
- [ ] Check layout and keyboard usability at common desktop and mobile viewport sizes.
- [ ] Fix discovered defects and rerun the relevant tests and manual checks.
- [ ] Record the verification steps and any known limitations in the README.

### Completion Criteria

The primary play flow and expected error cases work end to end, automated tests pass, and the browser has been checked at desktop and mobile sizes.

## Phase 5 — Cloud Deployment

### Tasks

- [ ] Select a cloud host that supports a Python Flask web service.
- [ ] Add the host-required startup command and production server dependency/configuration.
- [ ] Configure the service to install dependencies and serve the Flask app and static assets.
- [ ] Keep secrets and environment-specific settings out of source control.
- [ ] Deploy the application and confirm the public URL serves the browser client.
- [ ] Verify game creation, guessing, win/loss behavior, and API error responses against the deployed service.
- [ ] Document deployment configuration, launch steps, and the public URL in the README.

### Completion Criteria

The deployed URL serves a playable web-based Hangman game, with the browser communicating successfully with the Flask REST API.

## Explicitly Out of Scope

Do not implement or maintain tasks for these features as part of this assignment:

- Terminal client
- Automated or student bots
- Evaluation sessions or anti-cheating evaluation safeguards
- Scoring systems for bots or evaluations
- Leaderboards
- Bot tournament or performance analysis features

These features appeared in the broader project specification and prior roadmap but are excluded from this reduced project scope.

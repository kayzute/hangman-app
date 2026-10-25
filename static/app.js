const alphabet = 'abcdefghijklmnopqrstuvwxyz';
const difficultySelect = document.querySelector('#difficulty');
const newGameButton = document.querySelector('#new-game');
const keyboard = document.querySelector('#keyboard');
const patternNode = document.querySelector('#word-pattern');
const guessedNode = document.querySelector('#guessed-letters');
const incorrectNode = document.querySelector('#incorrect-letters');
const remainingNode = document.querySelector('#life-count');
const lengthNode = document.querySelector('#word-length');
const messageNode = document.querySelector('#game-message');
const footerNode = document.querySelector('#footer-status');
const captionNode = document.querySelector('#drawing-caption');
const drawingParts = [...document.querySelectorAll('.person-part')];
const faceParts = [...document.querySelectorAll('.cheek-dot, .smile')];

let gameId = null;
let gameState = null;
let busy = false;

function setMessage(text, kind = '') {
  messageNode.textContent = text;
  messageNode.className = `message${kind ? ` ${kind}` : ''}`;
}

function makeKeyboard() {
  keyboard.replaceChildren();
  for (const letter of alphabet) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'key';
    button.textContent = letter;
    button.setAttribute('aria-label', `Guess ${letter}`);
    button.addEventListener('click', () => submitGuess(letter));
    keyboard.append(button);
  }
}

function renderPattern(pattern) {
  patternNode.replaceChildren();
  for (const letter of pattern.split(' ')) {
    const slot = document.createElement('span');
    slot.className = `slot${letter === '_' ? '' : ' revealed'}`;
    slot.textContent = letter;
    patternNode.append(slot);
  }
  patternNode.setAttribute('aria-label', `Word pattern: ${pattern.replaceAll('_', 'blank')}`);
}

function render(state) {
  gameState = state;
  const guessed = state.guessed_letters || [];
  const incorrect = state.incorrect_letters || [];
  const finished = state.status !== 'playing';

  renderPattern(state.pattern);
  guessedNode.textContent = guessed.length ? guessed.join(' · ').toUpperCase() : '—';
  incorrectNode.textContent = incorrect.length ? incorrect.join(' · ').toUpperCase() : '—';
  remainingNode.textContent = `${state.remaining_guesses} / 6`;
  lengthNode.textContent = `${state.pattern.split(' ').length} letters`;

  const keys = keyboard.querySelectorAll('button');
  for (const key of keys) {
    const wasGuessed = guessed.includes(key.textContent);
    key.disabled = busy || !gameId || finished || wasGuessed;
    key.classList.toggle('wrong', wasGuessed && incorrect.includes(key.textContent));
    key.classList.toggle('correct', wasGuessed && !incorrect.includes(key.textContent));
  }

  drawingParts.forEach((part) => part.classList.toggle('visible', Number(part.dataset.part) <= incorrect.length));
  faceParts.forEach((part) => part.classList.toggle('visible', finished && state.status === 'won'));

  if (finished && state.status === 'won') {
    setMessage(`Lovely work — the word was ${state.word.toUpperCase()}.`, 'success');
    footerNode.textContent = 'A perfect little victory.';
    captionNode.textContent = 'The word has been found.';
  } else if (finished && state.status === 'lost') {
    setMessage(`The word was ${state.word.toUpperCase()}. Have another go?`, 'error');
    footerNode.textContent = 'Every word is a fresh start.';
    captionNode.textContent = 'This one got away.';
  } else {
    if (!messageNode.classList.contains('error')) setMessage(gameId ? 'Your turn — choose a letter.' : 'Choose a difficulty, then start a new game.');
    footerNode.textContent = gameId ? 'Keep this page open while you play.' : 'Ready when you are.';
    captionNode.textContent = state.remaining_guesses <= 2 ? 'Careful now, only a couple left.' : 'Six chances. Take your time.';
  }
}

async function requestJson(url, options) {
  const response = await fetch(url, options);
  let payload;
  try {
    payload = await response.json();
  } catch {
    throw new Error('The server sent an unreadable response. Please try again.');
  }
  if (!response.ok) throw new Error(payload.error || `Request failed (${response.status}).`);
  return payload;
}

async function startGame() {
  if (busy) return;
  busy = true;
  gameId = null;
  gameState = { pattern: '_ _ _ _ _', guessed_letters: [], incorrect_letters: [], remaining_guesses: 6, status: 'playing' };
  makeKeyboard();
  newGameButton.disabled = true;
  render(gameState);
  setMessage('Picking a word…');
  try {
    const state = await requestJson('/api/games', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ difficulty: difficultySelect.value }),
    });
    gameId = state.game_id;
    setMessage('Your turn — choose a letter.');
    render(state);
  } catch (error) {
    setMessage(error.message, 'error');
    footerNode.textContent = 'Check your connection and try again.';
  } finally {
    busy = false;
    newGameButton.disabled = false;
    if (gameState) render(gameState);
  }
}

async function submitGuess(letter) {
  if (busy || !gameId || !gameState || gameState.status !== 'playing') return;
  busy = true;
  render(gameState);
  try {
    const state = await requestJson(`/api/games/${encodeURIComponent(gameId)}/guess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ letter }),
    });
    setMessage('Your turn — choose a letter.');
    render(state);
  } catch (error) {
    setMessage(error.message, 'error');
  } finally {
    busy = false;
    if (gameState) render(gameState);
  }
}

newGameButton.addEventListener('click', startGame);
document.addEventListener('keydown', (event) => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.repeat) return;
  const letter = event.key.toLowerCase();
  if (alphabet.includes(letter) && letter.length === 1) submitGuess(letter);
});

makeKeyboard();

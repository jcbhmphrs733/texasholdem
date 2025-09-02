# Texas Hold'em Poker Engine

## Overview
This project is a modular, extensible Texas Hold'em poker simulation written in Python. It is designed for AI/ML research, bot development, and poker strategy experimentation. The engine supports multiple bots, robust betting logic, formatted output, and easy extensibility for new player strategies.

## Project Structure

```
texasholdem/
├── main.py               # Entry point for running the game
├── game_engine.py        # Core poker engine logic (betting, hand progression, pot management)
├── display.py            # Handles all formatted output (uses rich, but works in plain terminal)
├── game_state.py         # GameState class for round/stage management
├── bots/
│   ├── ParentBot.py      # Abstract base class for all bots
│   ├── Coyote.py         # Example bot implementation
│   └── ...               # Add your own bots here
└── ...
```

## How It Works
- **main.py**: Sets up the list of players (bots), then calls `play_hand(players)` from `game_engine.py` in a loop.
- **game_engine.py**: Handles all game logic: dealing, betting rounds, pot management, hand evaluation, player elimination, and dealer rotation. The main entry point is `play_hand(players)`.
- **display.py**: Provides all output formatting, including hand display, community cards, chip counts, and hand rankings.
- **game_state.py**: Defines the `GameState` class, which tracks the current stage, dealer, pot, and player states.
- **bots/**: Contains all bot/player logic. Each bot inherits from `ParentBot` and implements its own decision-making.

## Bot Classes and Methods

### ParentBot (Abstract Base Class)
Located in `bots/ParentBot.py`.

#### Key Methods:
- `make_decision(game_state) -> str`
  - **Purpose**: Given the current game state, return the action to take.
  - **Return**: One of: `'fold'`, `'call'`, `'check'`, `'raise'`, `'call and raise'`
- `observe(game_state) -> None`
  - **Purpose**: Observe the latest action and update internal state if needed.
- `receive_cards(cards: List[int]) -> None`
  - **Purpose**: Receive hole cards at the start of a hand.

#### Required Attributes:
- `name: str` — The bot's display name.
- `chips: int` — Current chip count.
- `hand: List[int]` — Current hole cards (treys format).
- `folded: bool` — Whether the player has folded this hand.
- `current_bet: int` — Amount currently bet this round.

#### Abstract Methods:
- `make_decision(game_state)` — Must be implemented by all bots.

### Example: Creating a New Bot
To create a new bot, inherit from `ParentBot` and implement the `make_decision` method. Example:

```python
from bots.ParentBot import ParentBot

class MyBot(ParentBot):
    def make_decision(self, game_state):
        # Access game_state attributes, e.g.:
        # game_state.pot, game_state.current_bet, game_state.stage, etc.
        # Return one of: 'fold', 'call', 'check', 'raise', 'call and raise'
        return 'call'
```

## GameState Object
The `game_state` object (from `game_state.py`) is passed to each bot's `make_decision` method. It provides:
- `players`: List of all player objects
- `dealer_index`: Index of the dealer
- `stage`: Current stage ('pre-flop', 'flop', 'turn', 'river')
- `pot`: Current pot size
- `current_bet`: Current bet to call
- `min_raise`: Minimum raise amount
- `bet_holder`: Player who last raised
- ...and more

## Tips for Creating Bots
- Always return a valid action string: `'fold'`, `'call'`, `'check'`, `'raise'`, or `'call and raise'`.
- Use the `game_state` object to access all relevant information about the hand, stage, and opponents.
- Implement the `observe` method if your bot needs to track opponent actions.
- Use the `receive_cards` method to store your hole cards at the start of each hand.
- Avoid using global state; keep all bot logic self-contained.

## Contributing
- Fork the repository and create a new branch for your bot or feature.
- Add new bots to the `bots/` directory, inheriting from `ParentBot`.
- Update the player list in `main.py` to include your bot for testing.
- Write clear, concise docstrings for all new methods and classes.
- Submit a pull request with a description of your changes.

## Requirements
- Python 3.8+
- [treys](https://github.com/ihendley/treys) (for poker hand evaluation)
- [rich](https://github.com/Textualize/rich) (for formatted output, optional)

## License
MIT License. See LICENSE file for details.

---
Feel free to expand this README with more details, examples, or documentation as the project evolves.
